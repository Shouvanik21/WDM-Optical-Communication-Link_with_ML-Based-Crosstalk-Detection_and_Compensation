import numpy as np


class CrosstalkModel:

    def __init__(self, coupling_coefficient=0.001):

        self.coupling_coefficient = coupling_coefficient

    # ======================================
    # Calculate crosstalk interference
    # ======================================

    def calculate_crosstalk(self, signals):

        number_of_channels = len(signals)

        crosstalk_signals = []

        for i in range(number_of_channels):

            # Start with no interference

            unwanted_signal = np.zeros_like(signals[i], dtype=float)

            # Other WDM channels contribute
            # unwanted optical energy

            for j in range(number_of_channels):

                # A channel does not interfere
                # with itself

                if i != j:

                    unwanted_signal += signals[j] * self.coupling_coefficient

            crosstalk_signals.append(unwanted_signal)

        return crosstalk_signals

    # ======================================
    # Add crosstalk to original signals
    # ======================================

    def add_crosstalk(self, signals):

        crosstalk_signals = self.calculate_crosstalk(signals)

        received_signals = []

        for i in range(len(signals)):

            received_signal = signals[i] + crosstalk_signals[i]

            received_signals.append(received_signal)

        return received_signals

    # ======================================
    # Calculate crosstalk power
    # ======================================

    def calculate_crosstalk_power(self, signals):

        crosstalk_signals = self.calculate_crosstalk(signals)

        powers = []

        for signal in crosstalk_signals:

            power = float(np.mean(signal**2))

            powers.append(power)

        return powers

    # ======================================
    # Calculate crosstalk ratio
    # ======================================

    def calculate_crosstalk_ratio(self, signals):

        crosstalk_signals = self.calculate_crosstalk(signals)

        ratios = []

        for i in range(len(signals)):

            signal_power = float(np.mean(signals[i] ** 2))

            interference_power = float(np.mean(crosstalk_signals[i] ** 2))

            epsilon = 1e-12

            ratio = interference_power / (signal_power + epsilon)

            ratios.append(ratio)

        return ratios

    # ======================================
    # Calculate crosstalk in dB
    # ======================================

    def calculate_crosstalk_db(self, signals):

        ratios = self.calculate_crosstalk_ratio(signals)

        crosstalk_db = []

        for ratio in ratios:

            epsilon = 1e-12

            value = 10 * np.log10(ratio + epsilon)

            crosstalk_db.append(float(value))

        return crosstalk_db
