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

        # --------------------------------
        # Generate channel signals
        # --------------------------------

        channel_bits = []

        channel_waveforms = []

        for i in range(self.number_of_channels):

            bits, waveform = self.generator.generate_signal()

            channel_bits.append(bits)

            channel_waveforms.append(waveform)

        # --------------------------------
        # Fiber transmission
        # --------------------------------

        fiber_signals = []

        for waveform in channel_waveforms:

            signal = self.fiber.transmit_signal(waveform)

            fiber_signals.append(signal)

        # --------------------------------
        # Crosstalk
        # --------------------------------

        crosstalk_model = CrosstalkModel(coupling_coefficient=self.coupling)

        crosstalk_signals = crosstalk_model.calculate_crosstalk(fiber_signals)

        signals_with_crosstalk = crosstalk_model.add_crosstalk(fiber_signals)

        # --------------------------------
        # Noise
        # --------------------------------

        noisy_signals = []

        for signal in signals_with_crosstalk:

            noise = np.random.normal(0, self.noise_level, len(signal))

            noisy_signal = signal + noise

            noisy_signals.append(noisy_signal)

        # --------------------------------
        # Receiver
        # --------------------------------

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

        # --------------------------------
        # Calculate measurements
        # --------------------------------

        fiber_loss = self.fiber.calculate_loss()

        dispersion_value = self.fiber.calculate_dispersion(wavelength_width=0.1)

        # Average crosstalk
        average_crosstalk = np.mean([np.mean(signal) for signal in crosstalk_signals])

        # Signal power
        signal_power = np.mean(fiber_signals[0] ** 2)

        # Noise power
        noise_power = self.noise_level**2

        if noise_power > 0:

            snr = signal_power / noise_power

            snr_db = 10 * np.log10(snr)

        else:

            snr_db = float("inf")

        # --------------------------------
        # Return everything
        # --------------------------------

        result = {
            "fiber_loss_db": fiber_loss,
            "dispersion_ps": dispersion_value,
            "crosstalk": self.coupling,
            "noise_level": self.noise_level,
            "snr_db": snr_db,
            "ber": float(np.mean(ber_values)),
            "channel_ber": ber_values,
            "received_power": float(np.mean(fiber_signals[0])),
            "bit_errors": int(np.sum(ber_values)),
        }

        return result
