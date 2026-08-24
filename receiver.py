class OpticalReceiver:

    def __init__(self, responsivity=0.8, sensitivity_dbm=-18):

        self.responsivity = responsivity

        self.sensitivity_dbm = sensitivity_dbm

    def dbm_to_watt(self, power_dbm):

        power_mw = 10 ** (power_dbm / 10)

        power_watt = power_mw / 1000

        return power_watt

    def convert_to_current(self, power_dbm):

        power_watt = self.dbm_to_watt(power_dbm)

        current = self.responsivity * power_watt

        return current

    def check_sensitivity(self, power_dbm):

        if power_dbm >= self.sensitivity_dbm:

            return "GOOD"

        else:

            return "LOW"
