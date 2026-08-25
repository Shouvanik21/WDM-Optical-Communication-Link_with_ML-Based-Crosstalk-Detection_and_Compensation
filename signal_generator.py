import numpy as np


class SignalGenerator:

    def __init__(self, number_of_bits=100, samples_per_bit=20, optical_power=0.001):

        self.number_of_bits = number_of_bits

        self.samples_per_bit = samples_per_bit

        # Optical power for binary 1
        # 0.001 W = 1 mW

        self.optical_power = optical_power

    # ======================================
    # Generate random digital bits
    # ======================================

    def generate_bits(self):

        bits = np.random.randint(0, 2, self.number_of_bits)

        return bits

    # ======================================
    # Convert bits into optical waveform
    # ======================================

    def bits_to_waveform(self, bits):

        waveform = np.repeat(bits, self.samples_per_bit)

        # Convert binary values into
        # optical power levels.
        #
        # Bit 0 -> 0 W
        # Bit 1 -> optical_power W

        waveform = waveform * self.optical_power

        return waveform

    # ======================================
    # Generate complete signal
    # ======================================

    def generate_signal(self):

        bits = self.generate_bits()

        waveform = self.bits_to_waveform(bits)

        return bits, waveform
