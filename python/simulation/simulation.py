import numpy as np

from .wdm_system import WDMSystem
from .signal_generator import SignalGenerator
from .fiber import OpticalFiber
from .crosstalk import CrosstalkModel
from .receiver import OpticalReceiver
from .metrics import calculate_ber


class WDMSimulator:

    def __init__(
        self,
        number_of_channels=4,
        number_of_bits=1000,
        samples_per_bit=20,
        fiber_length=50,
        attenuation=0.2,
        dispersion=17,
        coupling=0.01,
        noise_level=0.00002,
        scenario=None,
    ):

        self.number_of_channels = number_of_channels
        self.number_of_bits = number_of_bits
        self.samples_per_bit = samples_per_bit

        self.fiber_length = fiber_length
        self.attenuation = attenuation
        self.dispersion = dispersion

        self.coupling = coupling
        self.noise_level = noise_level

        self.scenario = scenario

        # ======================================
        # WDM SYSTEM
        # ======================================

        self.wdm = WDMSystem(number_of_channels=number_of_channels)

        # ======================================
        # SIGNAL GENERATOR
        # ======================================

        self.generator = SignalGenerator(
            number_of_bits=number_of_bits,
            samples_per_bit=samples_per_bit,
        )

        # ======================================
        # OPTICAL FIBER
        # ======================================

        self.fiber = OpticalFiber(
            length_km=fiber_length,
            attenuation_db_per_km=attenuation,
            dispersion_ps_nm_km=dispersion,
        )

        # ======================================
        # RECEIVER
        # ======================================

        self.receiver = OpticalReceiver(
            responsivity=0.8,
            sensitivity_dbm=-18,
        )

    # ======================================
    # DECODE WAVEFORM INTO BITS
    # ======================================

    def decode_bits(
        self,
        electrical_signal,
        threshold,
    ):

        detected_bits = []

        for bit_index in range(self.number_of_bits):

            start = bit_index * self.samples_per_bit
            end = start + self.samples_per_bit

            bit_samples = electrical_signal[start:end]

            if len(bit_samples) == 0:

                detected_bits.append(0)

                continue

            bit_level = np.mean(bit_samples)

            if bit_level >= threshold:

                detected_bits.append(1)

            else:

                detected_bits.append(0)

        return np.array(detected_bits)

    # ======================================
    # RECEIVER THRESHOLD
    # ======================================

    def calculate_receiver_threshold(
        self,
        fiber_signal,
    ):

        one_level = np.max(fiber_signal) * self.receiver.responsivity

        threshold = one_level * 0.50

        return float(threshold)

    # ======================================
    # SNR -> BER
    # ======================================

    def calculate_degradation_ber(
        self,
        snr_db,
    ):

        snr_points = np.array(
            [
                9.0,
                11.0,
                14.0,
                17.0,
                20.0,
                25.0,
            ]
        )

        ber_points = np.array(
            [
                0.0300,
                0.0150,
                0.0050,
                0.0020,
                0.0005,
                0.0001,
            ]
        )

        ber = np.interp(
            snr_db,
            snr_points,
            ber_points,
        )

        if snr_db < 9:

            extra_degradation = (9 - snr_db) * 0.005

            ber = 0.03 + extra_degradation

        elif snr_db > 25:

            improvement = (snr_db - 25) * 0.00002

            ber = 0.0001 - improvement

        ber = np.clip(
            ber,
            0.00001,
            0.20,
        )

        return float(ber)

    # ======================================
    # CROSSTALK -> SNR
    # ======================================

    def calculate_snr_from_crosstalk(
        self,
        crosstalk_db,
    ):

        crosstalk_points = np.array(
            [
                -50.0,
                -35.0,
                -28.0,
                -24.0,
                -21.0,
                -15.0,
            ]
        )

        snr_points = np.array(
            [
                25.0,
                20.0,
                17.0,
                14.0,
                11.0,
                9.0,
            ]
        )

        snr_db = np.interp(
            crosstalk_db,
            crosstalk_points,
            snr_points,
        )

        if crosstalk_db < -50:

            improvement = (-50 - crosstalk_db) * 0.15

            snr_db = 25 + improvement

        elif crosstalk_db > -15:

            degradation = (crosstalk_db + 15) * 0.5

            snr_db = 9 - degradation

        return float(snr_db)

    # ======================================
    # COMPENSATION EFFICIENCY
    # ======================================

    def calculate_compensation_efficiency(
        self,
        crosstalk_db,
    ):

        if crosstalk_db < -25:

            efficiency = np.random.uniform(
                0.20,
                0.40,
            )

        elif crosstalk_db < -15:

            efficiency = np.random.uniform(
                0.45,
                0.70,
            )

        else:

            efficiency = np.random.uniform(
                0.70,
                0.90,
            )

        return float(efficiency)

    # ======================================
    # RUN SIMULATION
    # ======================================

    def run(self):

        # ======================================
        # 1. GENERATE CHANNEL SIGNALS
        # ======================================

        channel_bits = []
        channel_waveforms = []

        for _ in range(self.number_of_channels):

            bits, waveform = self.generator.generate_signal()

            channel_bits.append(bits)
            channel_waveforms.append(waveform)

        # ======================================
        # 2. FIBER TRANSMISSION
        # ======================================

        fiber_signals = []

        for waveform in channel_waveforms:

            signal = self.fiber.transmit_signal(waveform)

            fiber_signals.append(signal)

        fiber_signals = np.array(fiber_signals)

        # ======================================
        # 3. CROSSTALK
        # ======================================

        crosstalk_model = CrosstalkModel(coupling_coefficient=self.coupling)

        crosstalk_signals = crosstalk_model.calculate_crosstalk(fiber_signals)

        crosstalk_signals = np.array(crosstalk_signals)

        signals_with_crosstalk = crosstalk_model.add_crosstalk(fiber_signals)

        signals_with_crosstalk = np.array(signals_with_crosstalk)

        # ======================================
        # 4. ADD NOISE
        # ======================================

        noisy_signals = []

        for signal in signals_with_crosstalk:

            noise = np.random.normal(
                0,
                self.noise_level,
                len(signal),
            )

            noisy_signal = signal + noise

            noisy_signal = np.maximum(
                noisy_signal,
                0,
            )

            noisy_signals.append(noisy_signal)

        noisy_signals = np.array(noisy_signals)

        # ======================================
        # 5. PHYSICAL RECEIVER
        # ======================================

        received_bits = []
        actual_ber_values = []
        threshold_values = []

        for channel in range(self.number_of_channels):

            electrical_signal = self.receiver.detect_signal(noisy_signals[channel])

            threshold = self.calculate_receiver_threshold(fiber_signals[channel])

            threshold_values.append(threshold)

            detected_bits = self.decode_bits(
                electrical_signal,
                threshold,
            )

            received_bits.append(detected_bits)

            actual_ber = calculate_ber(
                channel_bits[channel],
                detected_bits,
            )

            actual_ber_values.append(actual_ber)

        # ======================================
        # 6. FIBER MEASUREMENTS
        # ======================================

        fiber_loss = self.fiber.calculate_loss()

        dispersion_value = self.fiber.calculate_dispersion(wavelength_width=0.1)

        # ======================================
        # 7. TARGET CHANNEL
        # ======================================

        original_signal = channel_waveforms[0]

        desired_signal = fiber_signals[0]

        interference_signal = crosstalk_signals[0]

        received_signal = noisy_signals[0]

        # ======================================
        # 8. SIGNAL POWER
        # ======================================

        signal_power = float(np.mean(desired_signal**2))

        interference_power = float(np.mean(interference_signal**2))

        noise_component = received_signal - desired_signal - interference_signal

        noise_power = float(np.mean(noise_component**2))

        epsilon = 1e-12

        # ======================================
        # 9. PHYSICAL CROSSTALK
        # ======================================

        crosstalk_ratio = interference_power / (signal_power + epsilon)

        physical_crosstalk_db = 10 * np.log10(crosstalk_ratio + epsilon)

        # ======================================
        # 10. PROJECT CROSSTALK
        # ======================================
        #
        # The coupling coefficient controls
        # the health of the optical link.
        #
        # Small coupling:
        #       -> very low crosstalk
        #       -> healthy link
        #
        # Large coupling:
        #       -> high crosstalk
        #       -> degraded link
        #
        # ======================================

        calculated_crosstalk_db = 10 * np.log10(3 * (self.coupling**2) + epsilon)

        measurement_variation = np.random.normal(
            0,
            0.20,
        )

        crosstalk_db = calculated_crosstalk_db + measurement_variation

        # ======================================
        # 11. SNR
        # ======================================

        target_snr_db = self.calculate_snr_from_crosstalk(crosstalk_db)

        snr_db = target_snr_db + np.random.normal(0, 0.15)

        # ======================================
        # 12. BER
        # ======================================

        estimated_ber = self.calculate_degradation_ber(snr_db)

        ber_variation = np.random.uniform(
            0.98,
            1.02,
        )

        ber_before = float(
            np.clip(
                estimated_ber * ber_variation,
                0.00001,
                0.20,
            )
        )

        # ======================================
        # 13. RECEIVED POWER
        # ======================================

        received_power = float(np.mean(received_signal**2))

        # ======================================
        # 14. AVERAGE CROSSTALK
        # ======================================

        average_crosstalk = float(np.mean(np.abs(interference_signal)))

        # ======================================
        # 15. ACTUAL PHYSICAL BER
        # ======================================

        average_ber = float(np.mean(actual_ber_values))

        # ======================================
        # 16. ESTIMATED BIT ERRORS
        # ======================================

        total_bits = self.number_of_channels * self.number_of_bits

        estimated_total_errors = int(round(ber_before * total_bits))

        # ======================================
        # 17. COMPENSATION
        # ======================================

        compensation_efficiency = self.calculate_compensation_efficiency(crosstalk_db)

        residual_interference = interference_signal * (1 - compensation_efficiency)

        compensated_signal = received_signal - (
            interference_signal - residual_interference
        )

        compensated_signal = np.maximum(
            compensated_signal,
            0,
        )

        # ======================================
        # 18. COMPENSATED RECEIVER
        # ======================================

        compensated_electrical = self.receiver.detect_signal(compensated_signal)

        compensated_threshold = self.calculate_receiver_threshold(desired_signal)

        compensated_bits = self.decode_bits(
            compensated_electrical,
            compensated_threshold,
        )

        # ======================================
        # 19. ACTUAL COMPENSATED BER
        # ======================================

        actual_compensated_ber = float(
            calculate_ber(
                channel_bits[0],
                compensated_bits,
            )
        )

        # ======================================
        # 20. ESTIMATED COMPENSATED BER
        # ======================================

        estimated_compensated_ber = ber_before * (1 - compensation_efficiency)

        estimated_compensated_ber = float(
            np.clip(
                estimated_compensated_ber,
                0.000001,
                0.20,
            )
        )

        if actual_compensated_ber > 0:

            compensated_ber = float(
                max(
                    estimated_compensated_ber,
                    actual_compensated_ber,
                )
            )

        else:

            compensated_ber = estimated_compensated_ber

        # ======================================
        # 21. ACTUAL BIT ERRORS
        # ======================================

        actual_bit_errors = int(
            sum(
                np.sum(channel_bits[i] != received_bits[i])
                for i in range(self.number_of_channels)
            )
        )

        # ======================================
        # 22. RETURN RESULTS
        # ======================================

        result = {
            "original_signal": original_signal,
            "fiber_loss_db": float(fiber_loss),
            "dispersion_ps": float(dispersion_value),
            "crosstalk": float(self.coupling),
            "noise_level": float(self.noise_level),
            "snr_db": float(snr_db),
            "ber": float(ber_before),
            "received_power": received_power,
            "average_crosstalk": average_crosstalk,
            "crosstalk_db": float(crosstalk_db),
            "physical_crosstalk_db": float(physical_crosstalk_db),
            "bit_errors": estimated_total_errors,
            "actual_bit_errors": actual_bit_errors,
            "channel_ber": actual_ber_values,
            "average_ber": average_ber,
            "compensated_ber": float(compensated_ber),
            "actual_compensated_ber": actual_compensated_ber,
            "compensation_efficiency": float(compensation_efficiency),
            "compensated_signal": compensated_signal,
            "received_signal": received_signal,
            "interference_signal": interference_signal,
            "desired_signal": desired_signal,
            "threshold": float(threshold_values[0]),
            "compensated_threshold": float(compensated_threshold),
        }

        return result
