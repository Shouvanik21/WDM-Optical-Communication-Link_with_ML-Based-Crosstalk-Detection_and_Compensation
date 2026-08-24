import numpy as np

from wdm_system import WDMSystem
from fiber import OpticalFiber
from crosstalk import CrosstalkModel
from receiver import OpticalReceiver

print("\n==========================================")
print("   INTELLIGENT WDM OPTICAL LINK")
print("   ML-BASED CROSSTALK DETECTION")
print("==========================================\n")


# ==========================================
# 1. CREATE WDM SYSTEM
# ==========================================

wdm = WDMSystem(number_of_channels=4)

wdm.display_channels()


# ==========================================
# 2. CREATE OPTICAL FIBER
# ==========================================

fiber = OpticalFiber(length_km=50, attenuation_db_per_km=0.2, dispersion_ps_nm_km=17)


fiber_loss = fiber.calculate_loss()

dispersion = fiber.calculate_dispersion(wavelength_width=0.1)


print("\n========== FIBER ==========")

print("Fiber length:", fiber.length_km, "km")

print("Attenuation:", fiber.attenuation_db_per_km, "dB/km")

print("Total fiber loss:", fiber_loss, "dB")

print("Estimated dispersion:", dispersion, "ps")


# ==========================================
# 3. TRANSMITTER POWER
# ==========================================

transmit_power = wdm.transmit_power


print("\n========== TRANSMITTER ==========")

for i in range(len(transmit_power)):

    print("Channel", i + 1, "Transmit Power:", transmit_power[i], "dBm")


# ==========================================
# 4. FIBER TRANSMISSION
# ==========================================

received_power = []

for power in transmit_power:

    power_after_fiber = fiber.transmit(power)

    received_power.append(power_after_fiber)


received_power = np.array(received_power)


print("\n========== AFTER FIBER ==========")

for i in range(len(received_power)):

    print("Channel", i + 1, ":", round(received_power[i], 3), "dBm")


# ==========================================
# 5. CONVERT POWER FROM dBm TO mW
# ==========================================

received_power_mw = 10 ** (received_power / 10)


print("\n========== RECEIVED OPTICAL POWER ==========")

for i in range(len(received_power_mw)):

    print("Channel", i + 1, ":", round(received_power_mw[i], 6), "mW")


# ==========================================
# 6. CROSSTALK MODEL
# ==========================================

crosstalk_model = CrosstalkModel(coupling_coefficient=0.001)


crosstalk_power = crosstalk_model.calculate_crosstalk(received_power_mw)


print("\n========== CROSSTALK ==========")

for i in range(len(crosstalk_power)):

    print("Channel", i + 1, "Crosstalk Power:", round(crosstalk_power[i], 6), "mW")


# ==========================================
# 7. CROSSTALK IN dB
# ==========================================

print("\n========== CROSSTALK LEVEL ==========")

for i in range(len(received_power_mw)):

    xt_db = crosstalk_model.calculate_xt_db(received_power_mw[i], crosstalk_power[i])

    print("Channel", i + 1, "XT:", round(xt_db, 3), "dB")


# ==========================================
# 8. RECEIVER
# ==========================================

receiver = OpticalReceiver(responsivity=0.8, sensitivity_dbm=-18)


print("\n========== RECEIVER ==========")

for i in range(len(received_power)):

    current = receiver.convert_to_current(received_power[i])

    status = receiver.check_sensitivity(received_power[i])

    print(
        "Channel",
        i + 1,
        "| Power:",
        round(received_power[i], 3),
        "dBm",
        "| Current:",
        round(current * 1000, 6),
        "mA",
        "| Status:",
        status,
    )


print("\n==========================================")
print("        SIMULATION COMPLETE")
print("==========================================")
