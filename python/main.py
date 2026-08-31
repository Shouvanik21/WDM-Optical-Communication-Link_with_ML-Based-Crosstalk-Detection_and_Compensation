# This file creates an optical WDM system, runs the simulation,
# gives the resulting measurements to the trained ML model,
# determines the crosstalk severity, and performs compensation.

import os
import joblib
import sys
import random
from pathlib import Path

from simulation.simulation import WDMSimulator
from simulation.metrics import calculate_ber_improvement
from visualization.visualization import (
    plot_signals,
    plot_compensation,
)

# ======================================
# PROJECT PATHS
# ======================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "ml" / "wdm_crosstalk_model.pkl"


# ======================================
# LOAD MODEL
# ======================================

if not MODEL_FILE.exists():

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
# SELECT SIMULATION CONDITION
# ======================================

conditions = [
    ("NORMAL", 0.0001, 0.0049),
    ("WARNING", 0.0051, 0.0199),
    ("CRITICAL", 0.0201, 0.05),
]

condition_name, coupling_min, coupling_max = random.choice(conditions)

coupling = random.uniform(coupling_min, coupling_max)


print()
print("========== SIMULATION CONDITION ==========")
print("Expected Condition:", condition_name)
print(f"Coupling: {coupling:.6f}")


# ======================================
# CREATE SIMULATOR
# ======================================

simulator = WDMSimulator(
    number_of_channels=4,
    number_of_bits=1000,
    samples_per_bit=20,
    fiber_length=50,
    attenuation=0.2,
    dispersion=17,
    coupling=coupling,
    noise_level=0.00002,
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

print(f"Fiber Loss      : {result['fiber_loss_db']:.4f} dB")

print(f"Dispersion      : {result['dispersion_ps']:.4f} ps")

print(f"SNR             : {result['snr_db']:.4f} dB")

print(f"Received Power  : {result['received_power']:.10f}")

print(f"Noise Level     : {result['noise_level']:.10f}")

print(f"Crosstalk       : {result['crosstalk_db']:.4f} dB")

print(f"BER             : {result['ber']:.6f}")


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

print(f"Severity Detected : {severity}")

print(f"BER Before        : {ber_before:.6f}")

print(f"BER After         : {ber_after:.6f}")

print(f"BER Improvement   : {improvement:.2f}%")


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
# VISUALIZATION
# ======================================

if "--visualize" in sys.argv:

    print()
    print("Opening signal visualization...")

    plot_signals(
        original_signal=result["original_signal"],
        fiber_signal=result["desired_signal"],
        crosstalk_signal=(result["desired_signal"] + result["interference_signal"]),
        noisy_signal=result["received_signal"],
        number_of_samples=200,
    )

    # ======================================
    # BER VISUALIZATION
    # ======================================

    print()
    print("Opening BER compensation visualization...")

    plot_compensation(
        ber_before,
        ber_after,
    )
