import csv
import random

from simulation import WDMSimulator

# --------------------------------------
# Dataset settings
# --------------------------------------

NUMBER_OF_EXPERIMENTS = 1000


# --------------------------------------
# Decide system condition
# --------------------------------------


def classify_condition(ber):

    if ber < 0.001:

        return 0

    elif ber < 0.05:

        return 1

    else:

        return 2


# --------------------------------------
# Generate dataset
# --------------------------------------


def generate_dataset():

    rows = []

    for experiment in range(NUMBER_OF_EXPERIMENTS):

        # Random system parameters

        fiber_length = random.uniform(20, 100)

        coupling = random.uniform(0.0001, 0.05)

        noise_level = random.uniform(0.000001, 0.0001)

        # Create simulator

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

        # Run simulation

        result = simulator.run()

        # Get measurements

        ber = result["ber"]

        snr = result["snr_db"]

        fiber_loss = result["fiber_loss_db"]

        dispersion = result["dispersion_ps"]

        # Determine label

        label = classify_condition(ber)

        # Create dataset row

        row = [coupling, noise_level, snr, ber, fiber_loss, dispersion, label]

        rows.append(row)

    # ----------------------------------
    # Save CSV
    # ----------------------------------

    with open("wdm_dataset.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            ["crosstalk", "noise", "snr", "ber", "fiber_loss", "dispersion", "label"]
        )

        writer.writerows(rows)

    print("\nDataset generated successfully!")

    print("Experiments:", NUMBER_OF_EXPERIMENTS)


# --------------------------------------
# Start program
# --------------------------------------

if __name__ == "__main__":

    generate_dataset()
