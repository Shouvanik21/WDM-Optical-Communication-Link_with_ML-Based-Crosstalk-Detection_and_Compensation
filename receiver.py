import numpy as np


class OpticalReceiver:

    def __init__(self, responsivity=0.8, sensitivity_dbm=-18):

        self.responsivity = responsivity

        self.sensitivity_dbm = sensitivity_dbm

    def detect_signal(self, optical_signal):

        electrical_signal = optical_signal * self.responsivity

        return electrical_signal

    def make_decision(self, electrical_signal, threshold=0.00004):

        detected_bits = (electrical_signal >= threshold).astype(int)

        return detected_bits

    def dbm_to_watt(self, power_dbm):

        power_mw = 10 ** (power_dbm / 10)

        power_watt = power_mw / 1000

        return power_watt
