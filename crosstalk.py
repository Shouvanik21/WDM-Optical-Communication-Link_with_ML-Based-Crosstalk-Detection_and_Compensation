import numpy as np


class CrosstalkModel:

    def __init__(self, coupling_coefficient=0.001):

        self.coupling_coefficient = coupling_coefficient

    def calculate_crosstalk(self, signals):

        number_of_channels = len(signals)

        crosstalk_signals = []

        for i in range(number_of_channels):

            unwanted_signal = np.zeros_like(signals[i], dtype=float)

            for j in range(number_of_channels):

                if i != j:

                    unwanted_signal += signals[j] * self.coupling_coefficient

            crosstalk_signals.append(unwanted_signal)

        return crosstalk_signals

    def add_crosstalk(self, signals):

        crosstalk_signals = self.calculate_crosstalk(signals)

        received_signals = []

        for i in range(len(signals)):

            received_signal = signals[i] + crosstalk_signals[i]

            received_signals.append(received_signal)

        return received_signals
