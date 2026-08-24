import numpy as np


class WDMSystem:

    def __init__(self, number_of_channels=4):

        self.number_of_channels = number_of_channels

        # Wavelengths in nanometers
        self.wavelengths = np.array([1550, 1550.4, 1550.8, 1551.2])

        # Optical power of each transmitter in dBm at starting
        self.transmit_power = np.array([0, 0, 0, 0])

        # Channel spacing in GHz
        self.channel_spacing = 50

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
