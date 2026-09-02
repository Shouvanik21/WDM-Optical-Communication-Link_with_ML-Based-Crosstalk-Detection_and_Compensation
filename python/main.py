# ==========================================
# INTELLIGENT WDM OPTICAL COMMUNICATION
# ML-BASED CROSSTALK DETECTION
# AND COMPENSATION
# ==========================================

import sys
import random
import joblib
import pandas as pd

from pathlib import Path

from simulation.simulation import WDMSimulator
from simulation.metrics import calculate_ber_improvement

from visualization.visualization import (
    plot_signals,
    plot_compensation,
)

# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "ml" / "wdm_crosstalk_model.pkl"


# ==========================================
# CHECK MODEL
# ==========================================

if not MODEL_FILE.exists():

    print()
    print("ERROR: Model not found.")
    print("Run the model training script first.")

    raise SystemExit


# ==========================================
# LOAD ML MODEL
# ==========================================

model = joblib.load(MODEL_FILE)


# ==========================================
# HEADER
# ==========================================

print()

print("==========================================")
print("   INTELLIGENT WDM OPTICAL LINK")
print(" ML-BASED CROSSTALK DETECTION")
print("       AND COMPENSATION")
print("==========================================")


# ==========================================
# SIMULATION SCENARIOS
# ==========================================
#
# IMPORTANT:
#
# These are PHYSICAL operating conditions.
#
# They do NOT change the ML model.
#
# NORMAL:
# Very low coupling
# Very low crosstalk
#
# WARNING:
# Moderate coupling
# Moderate crosstalk
#
# CRITICAL:
# High coupling
# Severe crosstalk
#
# ==========================================

SCENARIO_COUPLING_RANGES = {
    "NORMAL": (
        0.0007,
        0.0012,
    ),
    "WARNING": (
        0.0120,
        0.0250,
    ),
    "CRITICAL": (
        0.0800,
        0.1500,
    ),
}


# ==========================================
# SELECT RANDOM SCENARIO
# ==========================================

scenario_names = [
    "NORMAL",
    "WARNING",
    "CRITICAL",
]

requested_scenario = random.choice(scenario_names)


# ==========================================
# SELECT COUPLING
# ==========================================

min_coupling, max_coupling = SCENARIO_COUPLING_RANGES[requested_scenario]

coupling = random.uniform(
    min_coupling,
    max_coupling,
)


# ==========================================
# NOISE LEVEL
# ==========================================
#
# Keep noise controlled.
#
# The main degradation mechanism in this
# project is crosstalk.
#
# ==========================================

noise_level = 0.00002


# ==========================================
# CREATE SIMULATOR
# ==========================================

simulator = WDMSimulator(
    number_of_channels=4,
    number_of_bits=1000,
    samples_per_bit=20,
    fiber_length=50,
    attenuation=0.2,
    dispersion=17,
    coupling=coupling,
    noise_level=noise_level,
    scenario=requested_scenario,
)


# ==========================================
# RUN PHYSICAL SIMULATION
# ==========================================

result = simulator.run()


# ==========================================
# PREPARE ML FEATURES
# ==========================================

features = pd.DataFrame(
    [
        {
            "snr_db": result["snr_db"],
            "received_power": result["received_power"],
            "noise_level": result["noise_level"],
            "fiber_loss_db": result["fiber_loss_db"],
            "dispersion_ps": result["dispersion_ps"],
            "average_crosstalk": result["average_crosstalk"],
            "crosstalk_db": result["crosstalk_db"],
            "ber": result["ber"],
        }
    ]
)


# ==========================================
# ML PREDICTION
# ==========================================

prediction = model.predict(features)[0]

probabilities = model.predict_proba(features)[0]


# ==========================================
# SEVERITY NAMES
# ==========================================

severity_names = {
    0: "NORMAL",
    1: "WARNING",
    2: "CRITICAL",
}


severity = severity_names[int(prediction)]


# ==========================================
# DISPLAY CONDITION
# ==========================================

print()

print("========== SIMULATION CONDITION ==========")

print(f"Generated Condition : " f"{requested_scenario}")

print(f"Coupling            : " f"{simulator.coupling:.6f}")


# ==========================================
# DISPLAY WDM CHANNELS
# ==========================================

simulator.wdm.display_channels()


# ==========================================
# DISPLAY RESULTS
# ==========================================

print()

print("========== OPTICAL LINK RESULTS ==========")

print(f"Fiber Loss       : " f"{result['fiber_loss_db']:.4f} dB")

print(f"Dispersion       : " f"{result['dispersion_ps']:.4f} ps")

print(f"SNR              : " f"{result['snr_db']:.4f} dB")

print(f"Received Power   : " f"{result['received_power']:.10f}")

print(f"Noise Level      : " f"{result['noise_level']:.10f}")

print(f"Crosstalk        : " f"{result['crosstalk_db']:.4f} dB")

print(f"Physical Crosstalk: " f"{result['physical_crosstalk_db']:.4f} dB")

print(f"Average Crosstalk: " f"{result['average_crosstalk']:.10f}")

print(f"BER              : " f"{result['ber']:.6f}")

print(f"Bit Errors       : " f"{result['bit_errors']}")


# ==========================================
# ML DETECTION
# ==========================================

print()

print("========== ML DETECTION ==========")

print(f"Predicted Severity: " f"{severity}")

print()

print("Prediction Confidence:")

for index, probability in enumerate(probabilities):

    print(f"{severity_names[index]:10s}: " f"{probability * 100:.2f}%")


# ==========================================
# COMPENSATION
# ==========================================

ber_before = float(result["ber"])

ber_after = float(result["compensated_ber"])

improvement = calculate_ber_improvement(
    ber_before,
    ber_after,
)


# ==========================================
# COMPENSATION OUTPUT
# ==========================================

print()

print("========== CROSSTALK COMPENSATION ==========")

print(f"Severity Detected : " f"{severity}")

print(f"BER Before        : " f"{ber_before:.6f}")

print(f"BER After         : " f"{ber_after:.6f}")

print(f"BER Improvement   : " f"{improvement:.2f}%")


# ==========================================
# SYSTEM STATUS
# ==========================================

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


# ==========================================
# OPTIONAL VISUALIZATION
# ==========================================

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

    print()

    print("Opening BER compensation visualization...")

    plot_compensation(
        ber_before,
        ber_after,
    )
