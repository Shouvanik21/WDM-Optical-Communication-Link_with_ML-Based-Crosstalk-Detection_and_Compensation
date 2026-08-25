import numpy as np


class OpticalReceiver:

    def __init__(self, responsivity=0.8, sensitivity_dbm=-18):

        self.responsivity = responsivity

        self.sensitivity_dbm = sensitivity_dbm

    # ======================================
    # Optical -> Electrical conversion
    # ======================================

    def detect_signal(self, optical_signal):

        electrical_signal = optical_signal * self.responsivity

        return electrical_signal

    # ======================================
    # Convert electrical waveform into
    # binary decisions
    # ======================================

    def make_decision(self, electrical_signal, threshold=None):

        # If no threshold is provided,
        # calculate it automatically.

        if threshold is None:

            minimum = np.min(electrical_signal)

            maximum = np.max(electrical_signal)

            # Midpoint between the lowest
            # and highest signal levels

            threshold = (minimum + maximum) / 2.0

        detected_bits = (electrical_signal >= threshold).astype(int)

        return detected_bits

    # ======================================
    # Calculate automatic threshold
    # ======================================

    def calculate_threshold(self, electrical_signal):

        minimum = np.min(electrical_signal)

        maximum = np.max(electrical_signal)

        threshold = (minimum + maximum) / 2.0

        return float(threshold)

    # ======================================
    # Convert dBm to Watts
    # ======================================

    def dbm_to_watt(self, power_dbm):

        power_mw = 10 ** (power_dbm / 10)

        power_watt = power_mw / 1000

        return power_watt

    # ======================================
    # Convert Watts to dBm
    # ======================================

    def watt_to_dbm(self, power_watt):

        epsilon = 1e-12

        power_mw = power_watt * 1000

        power_dbm = 10 * np.log10(power_mw + epsilon)

        return float(power_dbm)
