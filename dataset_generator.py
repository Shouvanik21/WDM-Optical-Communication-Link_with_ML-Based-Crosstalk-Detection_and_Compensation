import csv
import random

from simulation import WDMSimulator

SAMPLES_PER_CLASS = 1000


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


def generate_dataset():

    rows = []

    # ======================================
    # NORMAL
    # ======================================

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

    # Shuffle dataset

    random.shuffle(rows)

    # ======================================
    # SAVE CSV
    # ======================================

    with open("wdm_dataset.csv", "w", newline="") as file:

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

    print()

    print("Dataset generated successfully!")

    print("Total samples:", len(rows))

    print("NORMAL:", SAMPLES_PER_CLASS)

    print("WARNING:", SAMPLES_PER_CLASS)

    print("CRITICAL:", SAMPLES_PER_CLASS)


if __name__ == "__main__":

    generate_dataset()
