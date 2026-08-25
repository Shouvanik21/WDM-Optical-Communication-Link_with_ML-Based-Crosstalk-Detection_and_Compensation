import numpy as np

from wdm_system import WDMSystem
from signal_generator import SignalGenerator
from fiber import OpticalFiber
from crosstalk import CrosstalkModel
from receiver import OpticalReceiver

from metrics import calculate_ber


class WDMSimulator:

    def __init__(
        self,
        number_of_channels=4,
        number_of_bits=100,
        samples_per_bit=20,
        fiber_length=50,
        attenuation=0.2,
        dispersion=17,
        coupling=0.001,
        noise_level=0.000005,
    ):

        self.number_of_channels = number_of_channels
        self.number_of_bits = number_of_bits
        self.samples_per_bit = samples_per_bit

        self.fiber_length = fiber_length
        self.attenuation = attenuation
        self.dispersion = dispersion

        self.coupling = coupling
        self.noise_level = noise_level

        self.wdm = WDMSystem(number_of_channels=number_of_channels)

        self.generator = SignalGenerator(
            number_of_bits=number_of_bits, samples_per_bit=samples_per_bit
        )

        self.fiber = OpticalFiber(
            length_km=fiber_length,
            attenuation_db_per_km=attenuation,
            dispersion_ps_nm_km=dispersion,
        )

        self.receiver = OpticalReceiver(responsivity=0.8, sensitivity_dbm=-18)

    def run(self):

        # ======================================
        # 1. Generate channel signals
        # ======================================

        channel_bits = []
        channel_waveforms = []

        for i in range(self.number_of_channels):

            bits, waveform = self.generator.generate_signal()

            channel_bits.append(bits)
            channel_waveforms.append(waveform)

        # ======================================
        # 2. Fiber transmission
        # ======================================

        fiber_signals = []

        for waveform in channel_waveforms:

            signal = self.fiber.transmit_signal(waveform)

            fiber_signals.append(signal)

        fiber_signals = np.array(fiber_signals)

        # ======================================
        # 3. Crosstalk
        # ======================================

        crosstalk_model = CrosstalkModel(coupling_coefficient=self.coupling)

        crosstalk_signals = crosstalk_model.calculate_crosstalk(fiber_signals)

        crosstalk_signals = np.array(crosstalk_signals)

        signals_with_crosstalk = crosstalk_model.add_crosstalk(fiber_signals)

        signals_with_crosstalk = np.array(signals_with_crosstalk)

        # ======================================
        # 4. Add noise
        # ======================================

        noisy_signals = []

        for signal in signals_with_crosstalk:

            noise = np.random.normal(0, self.noise_level, len(signal))

            noisy_signal = signal + noise

            noisy_signals.append(noisy_signal)

        noisy_signals = np.array(noisy_signals)

        # ======================================
        # 5. Receiver
        # ======================================

        received_bits = []
        ber_values = []

        for channel in range(self.number_of_channels):

            electrical_signal = self.receiver.detect_signal(noisy_signals[channel])

            sample_bits = self.receiver.make_decision(electrical_signal)

            detected_bits = []

            for bit_index in range(self.number_of_bits):

                start = bit_index * self.samples_per_bit

                end = start + self.samples_per_bit

                samples = sample_bits[start:end]

                bit = int(np.mean(samples) >= 0.5)

                detected_bits.append(bit)

            detected_bits = np.array(detected_bits)

            received_bits.append(detected_bits)

            ber = calculate_ber(channel_bits[channel], detected_bits)

            ber_values.append(ber)

        # ======================================
        # 6. Fiber measurements
        # ======================================

        fiber_loss = self.fiber.calculate_loss()

        dispersion_value = self.fiber.calculate_dispersion(wavelength_width=0.1)

        # ======================================
        # 7. Target channel measurements
        # ======================================

        desired_signal = fiber_signals[0]

        interference_signal = crosstalk_signals[0]

        received_signal = noisy_signals[0]

        signal_power = float(np.mean(desired_signal**2))

        interference_power = float(np.mean(interference_signal**2))

        noise_power = float(self.noise_level**2)

        epsilon = 1e-12

        # ======================================
        # 8. SNR
        # ======================================

        snr = signal_power / (noise_power + epsilon)

        snr_db = 10 * np.log10(snr + epsilon)

        # ======================================
        # 9. Crosstalk ratio
        # ======================================

        crosstalk_ratio = interference_power / (signal_power + epsilon)

        crosstalk_db = 10 * np.log10(crosstalk_ratio + epsilon)

        # ======================================
        # 10. Received power
        # ======================================

        received_power = float(np.mean(received_signal**2))

        # ======================================
        # 11. Average crosstalk
        # ======================================

        average_crosstalk = float(np.mean(np.abs(crosstalk_signals)))

        # ======================================
        # 12. BER
        # ======================================

        average_ber = float(np.mean(ber_values))

        # ======================================
        # 13. Bit errors
        # ======================================

        total_bit_errors = int(
            sum(
                np.sum(channel_bits[i] != received_bits[i])
                for i in range(self.number_of_channels)
            )
        )

        # ======================================
        # 14. Crosstalk compensation
        # ======================================

        # In this simulation we know the
        # interference waveform exactly.
        #
        # A real system would estimate it.

        compensated_signal = received_signal - interference_signal

        # ======================================
        # 15. Compensated receiver
        # ======================================

        compensated_electrical = self.receiver.detect_signal(compensated_signal)

        compensated_sample_bits = self.receiver.make_decision(compensated_electrical)

        compensated_bits = []

        for bit_index in range(self.number_of_bits):

            start = bit_index * self.samples_per_bit

            end = start + self.samples_per_bit

            samples = compensated_sample_bits[start:end]

            bit = int(np.mean(samples) >= 0.5)

            compensated_bits.append(bit)

        compensated_bits = np.array(compensated_bits)

        compensated_ber = calculate_ber(channel_bits[0], compensated_bits)

        # ======================================
        # 16. Return results
        # ======================================

        result = {
            "fiber_loss_db": float(fiber_loss),
            "dispersion_ps": float(dispersion_value),
            "crosstalk": float(self.coupling),
            "noise_level": float(self.noise_level),
            "snr_db": float(snr_db),
            "ber": average_ber,
            "received_power": received_power,
            "average_crosstalk": average_crosstalk,
            "crosstalk_db": float(crosstalk_db),
            "bit_errors": total_bit_errors,
            "channel_ber": ber_values,
            "compensated_ber": float(compensated_ber),
            "compensated_signal": compensated_signal,
            "received_signal": received_signal,
            "interference_signal": interference_signal,
            "desired_signal": desired_signal,
        }

        return result
