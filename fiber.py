import numpy as np


class OpticalFiber:

    def __init__(self, length_km=50, attenuation_db_per_km=0.2, dispersion_ps_nm_km=17):

        self.length_km = length_km

        self.attenuation_db_per_km = attenuation_db_per_km

        self.dispersion_ps_nm_km = dispersion_ps_nm_km

    # ======================================
    # Calculate total fiber attenuation
    # ======================================

    def calculate_loss(self):

        loss = self.length_km * self.attenuation_db_per_km

        return float(loss)

    # ======================================
    # Calculate chromatic dispersion
    # ======================================

    def calculate_dispersion(self, wavelength_width):

        dispersion = abs(self.dispersion_ps_nm_km) * self.length_km * wavelength_width

        return float(dispersion)

    # ======================================
    # Convert fiber loss from dB into
    # linear power transmission factor
    # ======================================

    def get_power_factor(self):

        loss_db = self.calculate_loss()

        power_factor = 10 ** (-loss_db / 10)

        return float(power_factor)

    # ======================================
    # Transmit optical signal
    # ======================================

    def transmit_signal(self, signal):

        power_factor = self.get_power_factor()

        received_signal = np.asarray(signal) * power_factor

        return received_signal

    # ======================================
    # Calculate input signal power
    # ======================================

    def calculate_input_power(self, signal):

        signal = np.asarray(signal)

        power = np.mean(signal**2)

        return float(power)

    # ======================================
    # Calculate output signal power
    # ======================================

    def calculate_output_power(self, signal):

        transmitted_signal = self.transmit_signal(signal)

        power = np.mean(transmitted_signal**2)

        return float(power)
