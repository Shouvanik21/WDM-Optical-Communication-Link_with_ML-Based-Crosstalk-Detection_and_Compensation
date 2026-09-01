import csv
import numpy as np
from pathlib import Path

# ==========================================
# DATASET FILE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

filename = BASE_DIR / "wdm_dataset.csv"


# ==========================================
# STORAGE
# ==========================================

rows = []


# ==========================================
# READ DATASET
# ==========================================

print()

print("======================================")
print("       LOADING DATASET")
print("======================================")

if not filename.exists():

    print("ERROR: Dataset file not found!")
    print()

    print("Expected location:")
    print(filename)

    exit()


with open(filename, "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        rows.append(row)


# ==========================================
# CHECK DATASET
# ==========================================

if len(rows) == 0:

    print("ERROR: Dataset is empty!")
    exit()


# ==========================================
# COUNT CLASSES
# ==========================================

normal = 0
warning = 0
critical = 0


for row in rows:

    label = row["label"].strip().upper()

    if label == "NORMAL":

        normal += 1

    elif label == "WARNING":

        warning += 1

    elif label == "CRITICAL":

        critical += 1


# ==========================================
# FEATURE ARRAYS
# ==========================================

snr_values = np.array([float(row["snr_db"]) for row in rows])

crosstalk_values = np.array([float(row["crosstalk_db"]) for row in rows])

ber_values = np.array([float(row["ber"]) for row in rows])

received_power_values = np.array([float(row["received_power"]) for row in rows])

noise_values = np.array([float(row["noise_level"]) for row in rows])

fiber_loss_values = np.array([float(row["fiber_loss_db"]) for row in rows])

dispersion_values = np.array([float(row["dispersion_ps"]) for row in rows])

average_crosstalk_values = np.array([float(row["average_crosstalk"]) for row in rows])


# ==========================================
# PRINT DATASET ANALYSIS
# ==========================================

print()

print("======================================")
print("          DATASET ANALYSIS")
print("======================================")

print()

print("Dataset File:")
print(filename)

print()

print("Total samples :", len(rows))

print()

print("Class Counts:")

print("NORMAL        :", normal)

print("WARNING       :", warning)

print("CRITICAL      :", critical)

print("======================================")


# ==========================================
# CLASS PERCENTAGES
# ==========================================

total = len(rows)


if total > 0:

    normal_percent = (normal / total) * 100

    warning_percent = (warning / total) * 100

    critical_percent = (critical / total) * 100

    print()

    print("========== CLASS DISTRIBUTION ==========")

    print(f"NORMAL   : {normal_percent:.2f}%")

    print(f"WARNING  : {warning_percent:.2f}%")

    print(f"CRITICAL : {critical_percent:.2f}%")


# ==========================================
# FEATURE STATISTICS
# ==========================================

print()

print("========== FEATURE STATISTICS ==========")


# ==========================================
# SNR
# ==========================================

print()

print("SNR:")

print(f"  Minimum : " f"{np.min(snr_values):.4f} dB")

print(f"  Maximum : " f"{np.max(snr_values):.4f} dB")

print(f"  Average : " f"{np.mean(snr_values):.4f} dB")


# ==========================================
# CROSSTALK
# ==========================================

print()

print("Crosstalk:")

print(f"  Minimum : " f"{np.min(crosstalk_values):.4f} dB")

print(f"  Maximum : " f"{np.max(crosstalk_values):.4f} dB")

print(f"  Average : " f"{np.mean(crosstalk_values):.4f} dB")


# ==========================================
# BER
# ==========================================

print()

print("BER:")

print(f"  Minimum : " f"{np.min(ber_values):.7f}")

print(f"  Maximum : " f"{np.max(ber_values):.7f}")

print(f"  Average : " f"{np.mean(ber_values):.7f}")


# ==========================================
# RECEIVED POWER
# ==========================================

print()

print("Received Power:")

print(f"  Minimum : " f"{np.min(received_power_values):.4f}")

print(f"  Maximum : " f"{np.max(received_power_values):.4f}")

print(f"  Average : " f"{np.mean(received_power_values):.4f}")


# ==========================================
# NOISE LEVEL
# ==========================================

print()

print("Noise Level:")

print(f"  Minimum : " f"{np.min(noise_values):.8f}")

print(f"  Maximum : " f"{np.max(noise_values):.8f}")

print(f"  Average : " f"{np.mean(noise_values):.8f}")


# ==========================================
# FIBER LOSS
# ==========================================

print()

print("Fiber Loss:")

print(f"  Minimum : " f"{np.min(fiber_loss_values):.4f} dB")

print(f"  Maximum : " f"{np.max(fiber_loss_values):.4f} dB")

print(f"  Average : " f"{np.mean(fiber_loss_values):.4f} dB")


# ==========================================
# DISPERSION
# ==========================================

print()

print("Dispersion:")

print(f"  Minimum : " f"{np.min(dispersion_values):.4f}")

print(f"  Maximum : " f"{np.max(dispersion_values):.4f}")

print(f"  Average : " f"{np.mean(dispersion_values):.4f}")


# ==========================================
# AVERAGE CROSSTALK
# ==========================================

print()

print("Average Crosstalk:")

print(f"  Minimum : " f"{np.min(average_crosstalk_values):.4f}")

print(f"  Maximum : " f"{np.max(average_crosstalk_values):.4f}")

print(f"  Average : " f"{np.mean(average_crosstalk_values):.4f}")


# ==========================================
# CLASS-WISE ANALYSIS
# ==========================================

print()

print("========== CLASS-WISE ANALYSIS ==========")


for label in ["NORMAL", "WARNING", "CRITICAL"]:

    class_rows = [row for row in rows if row["label"].strip().upper() == label]

    if len(class_rows) == 0:

        continue

    class_snr = np.array([float(row["snr_db"]) for row in class_rows])

    class_crosstalk = np.array([float(row["crosstalk_db"]) for row in class_rows])

    class_ber = np.array([float(row["ber"]) for row in class_rows])

    print()

    print(label)

    print(f"  Samples       : " f"{len(class_rows)}")

    print(f"  Avg Crosstalk : " f"{np.mean(class_crosstalk):.4f} dB")

    print(f"  Avg SNR       : " f"{np.mean(class_snr):.4f} dB")

    print(f"  Avg BER       : " f"{np.mean(class_ber):.7f}")


# ==========================================
# REFERENCE CONDITION CHECK
# ==========================================

print()

print("========== REFERENCE CONDITIONS ==========")

print()

print("Expected relationship:")

print("Better link  -> More negative Crosstalk")

print("             -> Higher SNR")

print("             -> Lower BER")

print()

print("Worse link   -> Less negative Crosstalk")

print("             -> Lower SNR")

print("             -> Higher BER")


# ==========================================
# AUTOMATIC SANITY CHECK
# ==========================================

print()

print("========== DATASET SANITY CHECK ==========")


checks_passed = 0
checks_failed = 0


# ------------------------------------------
# Check 1: Class balance
# ------------------------------------------

if normal > 0 and warning > 0 and critical > 0:

    print("PASS: All three classes exist.")

    checks_passed += 1

else:

    print("FAIL: One or more classes are missing.")

    checks_failed += 1


# ------------------------------------------
# Check 2: Crosstalk ordering
# ------------------------------------------

normal_ct = np.mean(
    [float(row["crosstalk_db"]) for row in rows if row["label"].upper() == "NORMAL"]
)

warning_ct = np.mean(
    [float(row["crosstalk_db"]) for row in rows if row["label"].upper() == "WARNING"]
)

critical_ct = np.mean(
    [float(row["crosstalk_db"]) for row in rows if row["label"].upper() == "CRITICAL"]
)


if normal_ct < warning_ct < critical_ct:

    print("PASS: Crosstalk severity relationship is correct.")

    checks_passed += 1

else:

    print("FAIL: Crosstalk relationship is incorrect.")

    checks_failed += 1


# ------------------------------------------
# Check 3: SNR ordering
# ------------------------------------------

normal_snr = np.mean(
    [float(row["snr_db"]) for row in rows if row["label"].upper() == "NORMAL"]
)

warning_snr = np.mean(
    [float(row["snr_db"]) for row in rows if row["label"].upper() == "WARNING"]
)

critical_snr = np.mean(
    [float(row["snr_db"]) for row in rows if row["label"].upper() == "CRITICAL"]
)


if normal_snr > warning_snr > critical_snr:

    print("PASS: SNR severity relationship is correct.")

    checks_passed += 1

else:

    print("FAIL: SNR relationship is incorrect.")

    checks_failed += 1


# ------------------------------------------
# Check 4: BER ordering
# ------------------------------------------

normal_ber = np.mean(
    [float(row["ber"]) for row in rows if row["label"].upper() == "NORMAL"]
)

warning_ber = np.mean(
    [float(row["ber"]) for row in rows if row["label"].upper() == "WARNING"]
)

critical_ber = np.mean(
    [float(row["ber"]) for row in rows if row["label"].upper() == "CRITICAL"]
)


if normal_ber < warning_ber < critical_ber:

    print("PASS: BER severity relationship is correct.")

    checks_passed += 1

else:

    print("FAIL: BER relationship is incorrect.")

    checks_failed += 1


# ==========================================
# FINAL RESULT
# ==========================================

print()

print("======================================")

print(f"Checks Passed : {checks_passed}")

print(f"Checks Failed : {checks_failed}")


if checks_failed == 0:

    print()

    print("DATASET ANALYSIS: PASSED")

else:

    print()

    print("DATASET ANALYSIS: WARNING")


print("======================================")
