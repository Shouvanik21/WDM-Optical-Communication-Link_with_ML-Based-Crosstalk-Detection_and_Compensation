import csv
import random
import sys
from pathlib import Path

# ==========================================
# ADD PYTHON ROOT DIRECTORY TO PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ==========================================
# IMPORT SIMULATOR
# ==========================================

from simulation.simulation import WDMSimulator

# ==========================================
# SETTINGS
# ==========================================

SAMPLES_PER_CLASS = 1000


# ==========================================
# GENERATE ONE EXPERIMENT
# ==========================================


def generate_experiment(coupling_min, coupling_max):

    fiber_length = random.uniform(20, 100)

    coupling = random.uniform(coupling_min, coupling_max)

    noise_level = random.uniform(0.000001, 0.00002)

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

    return result


# ==========================================
# GENERATE DATASET
# ==========================================


def generate_dataset():

    rows = []

    # ======================================
    # NORMAL
    # ======================================

    print("Generating NORMAL samples...")

    for i in range(SAMPLES_PER_CLASS):

        result = generate_experiment(0.0001, 0.005)

        rows.append(
            [
                result["snr_db"],
                result["received_power"],
                result["noise_level"],
                result["fiber_loss_db"],
                result["dispersion_ps"],
                result["average_crosstalk"],
                result["crosstalk_db"],
                result["ber"],
                0,
            ]
        )

    # ======================================
    # WARNING
    # ======================================

    print("Generating WARNING samples...")

    for i in range(SAMPLES_PER_CLASS):

        result = generate_experiment(0.005, 0.02)

        rows.append(
            [
                result["snr_db"],
                result["received_power"],
                result["noise_level"],
                result["fiber_loss_db"],
                result["dispersion_ps"],
                result["average_crosstalk"],
                result["crosstalk_db"],
                result["ber"],
                1,
            ]
        )

    # ======================================
    # CRITICAL
    # ======================================

    print("Generating CRITICAL samples...")

    for i in range(SAMPLES_PER_CLASS):

        result = generate_experiment(0.02, 0.05)

        rows.append(
            [
                result["snr_db"],
                result["received_power"],
                result["noise_level"],
                result["fiber_loss_db"],
                result["dispersion_ps"],
                result["average_crosstalk"],
                result["crosstalk_db"],
                result["ber"],
                2,
            ]
        )

    # ======================================
    # SHUFFLE DATASET
    # ======================================

    random.shuffle(rows)

    # ======================================
    # SAVE DATASET
    # ======================================

    dataset_path = Path(__file__).resolve().parent / "wdm_dataset.csv"

    with open(dataset_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "snr",
                "received_power",
                "noise",
                "fiber_loss",
                "dispersion",
                "average_crosstalk",
                "crosstalk_db",
                "ber",
                "label",
            ]
        )

        writer.writerows(rows)

    # ======================================
    # RESULT
    # ======================================

    print()
    print("======================================")
    print("       DATASET GENERATED")
    print("======================================")

    print("Total samples:", len(rows))
    print("NORMAL:", SAMPLES_PER_CLASS)
    print("WARNING:", SAMPLES_PER_CLASS)
    print("CRITICAL:", SAMPLES_PER_CLASS)

    print()
    print("Dataset saved to:")
    print(dataset_path)

    print("======================================")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    generate_dataset()
