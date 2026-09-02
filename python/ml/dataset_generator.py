import csv
import random
from pathlib import Path

# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_FILE = BASE_DIR / "ml" / "wdm_dataset.csv"


# ==========================================
# DATASET SIZE
# ==========================================

SAMPLES_PER_CLASS = 1500


# ==========================================
# REFERENCE OPERATING POINTS
# ==========================================
#
# Crosstalk      SNR       BER
# --------------------------------
# -50 dB         25 dB     0.0001
# -35 dB         20 dB     0.0005
# -28 dB         17 dB     0.002
# -24 dB         14 dB     0.005
# -21 dB         11 dB     0.015
# -15 dB          9 dB     0.03
#
# ==========================================

REFERENCE_CROSSTALK = [
    -50.0,
    -35.0,
    -28.0,
    -24.0,
    -21.0,
    -15.0,
]

REFERENCE_SNR = [
    25.0,
    20.0,
    17.0,
    14.0,
    11.0,
    9.0,
]

REFERENCE_BER = [
    0.0001,
    0.0005,
    0.002,
    0.005,
    0.015,
    0.03,
]


# ==========================================
# CLASSIFICATION
# ==========================================
#
# We keep the same basic condition:
#
# CRITICAL:
# severe degradation
#
# WARNING:
# moderate degradation
#
# NORMAL:
# healthy optical link
#
# ==========================================


def classify_condition(snr, crosstalk, ber):

    # --------------------------------------
    # CRITICAL
    # --------------------------------------

    if snr < 10 or crosstalk > -15 or ber > 0.01:

        return 2, "CRITICAL"

    # --------------------------------------
    # WARNING
    # --------------------------------------

    if snr <= 25 or crosstalk >= -25 or ber >= 0.001:

        return 1, "WARNING"

    # --------------------------------------
    # NORMAL
    # --------------------------------------

    return 0, "NORMAL"


# ==========================================
# LINEAR INTERPOLATION
# ==========================================


def interpolate(
    x,
    x_points,
    y_points,
):

    # --------------------------------------
    # BELOW RANGE
    # --------------------------------------

    if x <= x_points[0]:

        slope = (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])

        return y_points[0] + slope * (x - x_points[0])

    # --------------------------------------
    # ABOVE RANGE
    # --------------------------------------

    if x >= x_points[-1]:

        slope = (y_points[-1] - y_points[-2]) / (x_points[-1] - x_points[-2])

        return y_points[-1] + slope * (x - x_points[-1])

    # --------------------------------------
    # BETWEEN POINTS
    # --------------------------------------

    for i in range(len(x_points) - 1):

        x1 = x_points[i]
        x2 = x_points[i + 1]

        y1 = y_points[i]
        y2 = y_points[i + 1]

        if x1 <= x <= x2:

            ratio = (x - x1) / (x2 - x1)

            return y1 + ratio * (y2 - y1)

    return y_points[-1]


# ==========================================
# SNR FROM CROSSTALK
# ==========================================


def calculate_snr(crosstalk):

    return interpolate(
        crosstalk,
        REFERENCE_CROSSTALK,
        REFERENCE_SNR,
    )


# ==========================================
# BER FROM SNR
# ==========================================


def calculate_ber(snr):

    snr_points = [
        9.0,
        11.0,
        14.0,
        17.0,
        20.0,
        25.0,
    ]

    ber_points = [
        0.03,
        0.015,
        0.005,
        0.002,
        0.0005,
        0.0001,
    ]

    ber = interpolate(
        snr,
        snr_points,
        ber_points,
    )

    return max(
        1e-7,
        ber,
    )


# ==========================================
# CROSSTALK RANGE
# ==========================================
#
# IMPORTANT:
#
# These ranges are now aligned with the
# actual simulation formula:
#
# crosstalk_db =
# 10 * log10(3 * coupling^2)
#
#
# NORMAL
# -------
# We deliberately keep crosstalk
# comfortably below -50 dB.
#
# This guarantees:
#
# SNR > 25 dB
# BER < 0.001
#
#
# WARNING
# -------
# Moderate degradation.
#
#
# CRITICAL
# --------
# Strong degradation.
#
# ==========================================


def generate_crosstalk_candidate(class_name):

    if class_name == "NORMAL":

        return random.uniform(
            -60.0,
            -51.0,
        )

    if class_name == "WARNING":

        return random.uniform(
            -49.0,
            -22.5,
        )

    # --------------------------------------
    # CRITICAL
    # --------------------------------------

    return random.uniform(
        -22.0,
        -5.0,
    )


# ==========================================
# GENERATE RECEIVED POWER
# ==========================================
#
# The real simulation uses:
#
# optical_power = 0.001 W
#
# 50 km fiber with 10 dB loss:
#
# power factor = 0.1
#
# Therefore the received waveform is
# around 0.0001 W for a binary 1.
#
# The simulator calculates:
#
# mean(signal^2)
#
# With approximately 50% ones:
#
# received power is around:
#
# 5e-9
#
# ==========================================


def generate_received_power():

    return random.uniform(
        4.0e-9,
        6.0e-9,
    )


# ==========================================
# GENERATE AVERAGE CROSSTALK
# ==========================================
#
# Match the physical simulator.
#
# Approximately:
#
# average crosstalk
# ≈ received amplitude
#   × coupling
#   × average channel activity
#
# ==========================================


def generate_average_crosstalk(
    received_power,
    crosstalk,
):

    # Convert crosstalk dB to amplitude ratio.
    #
    # This follows the same general amplitude
    # relationship used by the optical signal.

    amplitude_ratio = 10 ** (crosstalk / 20)

    received_amplitude = received_power**0.5

    average_crosstalk = received_amplitude * amplitude_ratio

    return average_crosstalk


# ==========================================
# GENERATE ONE VALID SAMPLE
# ==========================================


def generate_sample(requested_class):

    while True:

        # ----------------------------------
        # CROSSTALK
        # ----------------------------------

        crosstalk = generate_crosstalk_candidate(requested_class)

        # ----------------------------------
        # SNR
        # ----------------------------------

        snr = calculate_snr(crosstalk)

        snr += random.gauss(
            0,
            0.15,
        )

        # ----------------------------------
        # BER
        # ----------------------------------

        ber = calculate_ber(snr)

        ber *= random.uniform(
            0.95,
            1.05,
        )

        ber = max(
            1e-7,
            ber,
        )

        # ----------------------------------
        # CLASSIFY
        # ----------------------------------

        severity, label = classify_condition(
            snr,
            crosstalk,
            ber,
        )

        # ----------------------------------
        # ACCEPT ONLY REQUESTED CLASS
        # ----------------------------------

        if label != requested_class:

            continue

        # ----------------------------------
        # FIBER LOSS
        # ----------------------------------

        fiber_loss = random.uniform(
            9.8,
            10.2,
        )

        # ----------------------------------
        # DISPERSION
        # ----------------------------------

        dispersion = random.uniform(
            83.0,
            87.0,
        )

        # ----------------------------------
        # NOISE
        # ----------------------------------

        noise_level = random.uniform(
            0.000018,
            0.000022,
        )

        # ----------------------------------
        # RECEIVED POWER
        # ----------------------------------

        received_power = generate_received_power()

        # ----------------------------------
        # AVERAGE CROSSTALK
        # ----------------------------------

        average_crosstalk = generate_average_crosstalk(
            received_power,
            crosstalk,
        )

        # ----------------------------------
        # RETURN SAMPLE
        # ----------------------------------

        return [
            round(
                snr,
                6,
            ),
            received_power,
            noise_level,
            fiber_loss,
            dispersion,
            average_crosstalk,
            round(
                crosstalk,
                6,
            ),
            ber,
            severity,
            label,
        ]


# ==========================================
# DATASET GENERATION
# ==========================================

rows = []


print()

print("==========================================")

print("       GENERATING WDM DATASET")

print("==========================================")


# ==========================================
# GENERATE EXACTLY 1500 PER CLASS
# ==========================================

for class_name in [
    "NORMAL",
    "WARNING",
    "CRITICAL",
]:

    print(f"Generating {class_name} samples...")

    class_rows = []

    while len(class_rows) < SAMPLES_PER_CLASS:

        sample = generate_sample(class_name)

        class_rows.append(sample)

    rows.extend(class_rows)


# ==========================================
# SHUFFLE
# ==========================================

random.shuffle(rows)


# ==========================================
# WRITE CSV
# ==========================================

with open(
    DATASET_FILE,
    "w",
    newline="",
) as file:

    writer = csv.writer(file)

    writer.writerow(
        [
            "snr_db",
            "received_power",
            "noise_level",
            "fiber_loss_db",
            "dispersion_ps",
            "average_crosstalk",
            "crosstalk_db",
            "ber",
            "severity",
            "label",
        ]
    )

    writer.writerows(rows)


# ==========================================
# VERIFY DATASET
# ==========================================

normal_count = sum(1 for row in rows if row[8] == 0)

warning_count = sum(1 for row in rows if row[8] == 1)

critical_count = sum(1 for row in rows if row[8] == 2)


# ==========================================
# SUMMARY
# ==========================================

print()

print("==========================================")

print("       WDM DATASET GENERATED")

print("==========================================")

print(f"Dataset : {DATASET_FILE}")

print(f"Samples : {len(rows)}")

print()

print(f"NORMAL   : {normal_count}")

print(f"WARNING  : {warning_count}")

print(f"CRITICAL : {critical_count}")

print()

print("Expected Distribution:")

print(f"NORMAL   : {SAMPLES_PER_CLASS}")

print(f"WARNING  : {SAMPLES_PER_CLASS}")

print(f"CRITICAL : {SAMPLES_PER_CLASS}")

print()

print("Classification Rules:")

print("NORMAL   : " "SNR > 25 AND " "Crosstalk < -25 AND " "BER < 0.001")

print("WARNING  : " "SNR <= 25 OR " "Crosstalk >= -25 OR " "BER >= 0.001")

print("CRITICAL : " "SNR < 10 OR " "Crosstalk > -15 OR " "BER > 0.01")

print()

if (
    normal_count == SAMPLES_PER_CLASS
    and warning_count == SAMPLES_PER_CLASS
    and critical_count == SAMPLES_PER_CLASS
):

    print("✓ Dataset is perfectly balanced.")

else:

    print("WARNING: Dataset is not balanced.")

print()

print("Dataset generation completed.")
