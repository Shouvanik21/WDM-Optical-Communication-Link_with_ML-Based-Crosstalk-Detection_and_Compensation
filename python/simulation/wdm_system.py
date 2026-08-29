import numpy as np


class WDMSystem:

    def __init__(self, number_of_channels=4):

        self.number_of_channels = number_of_channels

        # ======================================
        # WDM wavelengths
        # ======================================
        #
        # Four optical channels are placed at
        # different wavelengths.
        #
        # Channel 1 -> 1550.0 nm
        # Channel 2 -> 1550.4 nm
        # Channel 3 -> 1550.8 nm
        # Channel 4 -> 1551.2 nm
        #
        # Spacing = 0.4 nm
        #

        base_wavelength = 1550.0

        wavelength_spacing = 0.4

        self.wavelengths = (
            base_wavelength + np.arange(self.number_of_channels) * wavelength_spacing
        )

        # ======================================
        # Transmitter optical power
        # ======================================
        #
        # 0 dBm = 1 mW
        #

        self.transmit_power = np.zeros(self.number_of_channels)

        # ======================================
        # Channel spacing
        # ======================================

        self.channel_spacing = 50

    # ==========================================
    # Display WDM channels
    # ==========================================

    def display_channels(self):

        print("\n========== WDM CHANNELS ==========")

        for i in range(self.number_of_channels):

            print(
                "Channel",
                i + 1,
                "| Wavelength =",
                self.wavelengths[i],
                "nm",
                "| Power =",
                self.transmit_power[i],
                "dBm",
            )

        print("Channel spacing:", self.channel_spacing, "GHz")

    # ==========================================
    # Get wavelength of a channel
    # ==========================================

    def get_wavelength(self, channel):

        if channel < 0 or channel >= self.number_of_channels:

            raise ValueError("Invalid channel number.")

        return float(self.wavelengths[channel])

    # ==========================================
    # Get all wavelengths
    # ==========================================

    def get_wavelengths(self):

        return self.wavelengths.copy()

    # ==========================================
    # Get transmitter power
    # ==========================================

    def get_transmit_power(self, channel):

        if channel < 0 or channel >= self.number_of_channels:

            raise ValueError("Invalid channel number.")

        return float(self.transmit_power[channel])

    # ==========================================
    # Convert dBm to Watts
    # ==========================================

    def dbm_to_watt(self, power_dbm):

        power_mw = 10 ** (power_dbm / 10)

        power_watt = power_mw / 1000

        return float(power_watt)
