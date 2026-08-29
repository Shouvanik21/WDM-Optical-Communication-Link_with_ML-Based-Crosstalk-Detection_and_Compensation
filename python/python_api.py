import sys
import json
import joblib
import numpy as np
from pathlib import Path

from simulation.simulation import WDMSimulator


# ----------------------------------------
# Project paths
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "ml" / "wdm_crosstalk_model.pkl"


# ----------------------------------------
# Load trained ML model
# ----------------------------------------

model = joblib.load(MODEL_FILE)


# ----------------------------------------
# Run optical simulation
# ----------------------------------------


def run_simulation(fiber_length=50, coupling=0.01, noise_level=0.000005):

    simulator = WDMSimulator(
        number_of_channels=4,
        number_of_bits=100,
        samples_per_bit=20,
        fiber_length=fiber_length,
        attenuation=0.2,
        dispersion=17,
        coupling=coupling,
        noise_level=noise_level,
    )

    result = simulator.run()

    # ----------------------------------------
    # Prepare ML features
    # ----------------------------------------

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

    # ----------------------------------------
    # ML prediction
    # ----------------------------------------

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    labels = {
        0: "NORMAL",
        1: "WARNING",
        2: "CRITICAL",
    }

    severity = labels[int(prediction)]

    confidence = {
        "NORMAL": float(probabilities[0] * 100),
        "WARNING": float(probabilities[1] * 100),
        "CRITICAL": float(probabilities[2] * 100),
    }

    # ----------------------------------------
    # Return frontend-friendly data
    # ----------------------------------------

    response = {
        "fiber_loss_db": float(result["fiber_loss_db"]),
        "dispersion_ps": float(result["dispersion_ps"]),
        "snr_db": float(result["snr_db"]),
        "ber": float(result["ber"]),
        "crosstalk_db": float(result["crosstalk_db"]),
        "average_crosstalk": float(result["average_crosstalk"]),
        "noise_level": float(result["noise_level"]),
        "received_power": float(result["received_power"]),
        "severity": severity,
        "confidence": confidence,
        "compensated_ber": float(result["compensated_ber"]),
        "bit_errors": int(result["bit_errors"]),
        "channel_ber": [float(value) for value in result["channel_ber"]],
    }

    return response


# ----------------------------------------
# Read parameters from Node
# ----------------------------------------

if __name__ == "__main__":

    try:

        input_data = sys.stdin.read()

        if input_data:

            parameters = json.loads(input_data)

        else:

            parameters = {}

        fiber_length = float(parameters.get("fiber_length", 50))

        coupling = float(parameters.get("coupling", 0.01))

        noise_level = float(parameters.get("noise_level", 0.000005))

        result = run_simulation(
            fiber_length=fiber_length, coupling=coupling, noise_level=noise_level
        )

        print(json.dumps(result))

    except Exception as error:

        print(json.dumps({"error": str(error)}))

        sys.exit(1)
