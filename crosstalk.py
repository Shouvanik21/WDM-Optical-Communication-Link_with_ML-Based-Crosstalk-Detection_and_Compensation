import numpy as np


class CrosstalkModel:

    def __init__(self, coupling_coefficient=0.001):

        #The coefficient tells us how much unwanted power from another channel contributes to the victim channel in our simplified model.
        self.coupling_coefficient = coupling_coefficient

    def calculate_crosstalk(self, powers_mw):

        #powers_mw contains power of all channels currently
        number_of_channels = len(powers_mw)

        #creates a list of empty values like np.zeros(4)=>[0,0,0,0]
        crosstalk_power = np.zeros(number_of_channels)

        #calculate crosstalk for every channel
        for i in range(number_of_channels):

            unwanted_power = 0

            #for each victim channel check every other channel
            for j in range(number_of_channels):

                if i != j:

                    unwanted_power += powers_mw[j] * self.coupling_coefficient

            crosstalk_power[i] = unwanted_power

        return crosstalk_power

    #This converts crosstalk to dB relative to the desired signal.
    def calculate_xt_db(self, signal_power, crosstalk_power):

        if crosstalk_power <= 0:

            return -100

        xt_ratio = crosstalk_power / signal_power

        xt_db = 10 * np.log10(xt_ratio)

        return xt_db
