import numpy as np


class SignalGenerator:

    def __init__(self, number_of_bits=100, samples_per_bit=20):

        self.number_of_bits = number_of_bits
        self.samples_per_bit = samples_per_bit

    def generate_bits(self):

        bits = np.random.randint(0, 2, self.number_of_bits)

        return bits

    def bits_to_waveform(self, bits):

        waveform = np.repeat(bits, self.samples_per_bit)

        return waveform

    def generate_signal(self):

        bits = self.generate_bits()

        waveform = self.bits_to_waveform(bits)

        return bits, waveform
