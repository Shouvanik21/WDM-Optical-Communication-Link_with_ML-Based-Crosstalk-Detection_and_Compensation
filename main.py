import os
import joblib

from simulation import WDMSimulator
from metrics import calculate_ber_improvement
from visualization import plot_compensation

MODEL_FILE = "wdm_crosstalk_model.pkl"


# ======================================
# LOAD MODEL
# ======================================

if not os.path.exists(MODEL_FILE):

    print()

    print("ERROR: Model not found.")

    print("Run train_model.py first.")

    raise SystemExit


model = joblib.load(MODEL_FILE)


# ======================================
# HEADER
# ======================================

print()

print("==========================================")

print("   INTELLIGENT WDM OPTICAL LINK")

print(" ML-BASED CROSSTALK DETECTION")

print("       AND COMPENSATION")

print("==========================================")


# ======================================
# SIMULATOR
# ======================================

simulator = WDMSimulator(
    number_of_channels=4,
    number_of_bits=100,
    samples_per_bit=20,
    fiber_length=50,
    attenuation=0.2,
    dispersion=17,
    coupling=0.01,
    noise_level=0.000005,
)


# ======================================
# RUN SIMULATION
# ======================================

result = simulator.run()


# ======================================
# DISPLAY CHANNELS
# ======================================

simulator.wdm.display_channels()


# ======================================
# DISPLAY LINK RESULTS
# ======================================

print()

print("========== OPTICAL LINK RESULTS ==========")


print(f"Fiber Loss      : " f"{result['fiber_loss_db']:.4f} dB")


print(f"Dispersion      : " f"{result['dispersion_ps']:.4f} ps")


print(f"SNR             : " f"{result['snr_db']:.4f} dB")


print(f"Received Power  : " f"{result['received_power']:.10f}")


print(f"Noise Level     : " f"{result['noise_level']:.10f}")


print(f"Crosstalk       : " f"{result['crosstalk_db']:.4f} dB")


print(f"BER             : " f"{result['ber']:.6f}")


# ======================================
# ML FEATURES
# ======================================

features = [
    [
        result["snr_db"],
        result["received_power"],
        result["noise_level"],
        result["fiber_loss_db"],
        result["dispersion_ps"],
        result["average_crosstalk"],
        result["crosstalk_db"],
        result["ber"],
    ]
]


# ======================================
# ML PREDICTION
# ======================================

prediction = model.predict(features)[0]


probabilities = model.predict_proba(features)[0]


severity_names = {0: "NORMAL", 1: "WARNING", 2: "CRITICAL"}


severity = severity_names[int(prediction)]


# ======================================
# ML RESULT
# ======================================

print()

print("========== ML DETECTION ==========")


print("Predicted Severity:", severity)


print()

print("Prediction Confidence:")


for index, probability in enumerate(probabilities):

    print(f"{severity_names[index]:10s}: " f"{probability * 100:.2f}%")


# ======================================
# COMPENSATION
# ======================================

ber_before = result["ber"]


ber_after = result["compensated_ber"]


improvement = calculate_ber_improvement(ber_before, ber_after)


print()

print("========== CROSSTALK COMPENSATION ==========")


print(f"Severity Detected : " f"{severity}")


print(f"BER Before        : " f"{ber_before:.6f}")


print(f"BER After         : " f"{ber_after:.6f}")


print(f"BER Improvement   : " f"{improvement:.2f}%")


# ======================================
# FINAL STATUS
# ======================================

print()

print("==========================================")

print("             SYSTEM STATUS")

print("==========================================")


if severity == "NORMAL":

    print("Optical link operating normally.")


elif severity == "WARNING":

    print("Moderate crosstalk detected.")


else:

    print("Severe crosstalk detected!")


print("ML detection completed.")


print("Crosstalk compensation completed.")


print("==========================================")


# ======================================
# BER VISUALIZATION
# ======================================

plot_compensation(ber_before, ber_after)
