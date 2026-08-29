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

with open(filename, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        rows.append(row)


# ==========================================
# COUNT CLASSES
# ==========================================

normal = 0
warning = 0
critical = 0


for row in rows:

    label = int(row["label"])

    if label == 0:

        normal += 1

    elif label == 1:

        warning += 1

    elif label == 2:

        critical += 1


# ==========================================
# FEATURE ARRAYS
# ==========================================

snr_values = np.array([float(row["snr"]) for row in rows])


crosstalk_values = np.array([float(row["crosstalk_db"]) for row in rows])


ber_values = np.array([float(row["ber"]) for row in rows])


fiber_loss_values = np.array([float(row["fiber_loss"]) for row in rows])


# ==========================================
# PRINT DATASET ANALYSIS
# ==========================================

print()

print("======================================")

print("          DATASET ANALYSIS")

print("======================================")


print("Total samples :", len(rows))


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

    print("Class Distribution:")

    print(f"NORMAL   : " f"{normal_percent:.2f}%")

    print(f"WARNING  : " f"{warning_percent:.2f}%")

    print(f"CRITICAL : " f"{critical_percent:.2f}%")


# ==========================================
# FEATURE STATISTICS
# ==========================================

print()

print("========== FEATURE STATISTICS ==========")


print(f"SNR:")

print(f"  Minimum : " f"{np.min(snr_values):.4f}")

print(f"  Maximum : " f"{np.max(snr_values):.4f}")

print(f"  Average : " f"{np.mean(snr_values):.4f}")


print()

print("Crosstalk:")

print(f"  Minimum : " f"{np.min(crosstalk_values):.4f} dB")

print(f"  Maximum : " f"{np.max(crosstalk_values):.4f} dB")

print(f"  Average : " f"{np.mean(crosstalk_values):.4f} dB")


print()

print("BER:")

print(f"  Minimum : " f"{np.min(ber_values):.6f}")

print(f"  Maximum : " f"{np.max(ber_values):.6f}")

print(f"  Average : " f"{np.mean(ber_values):.6f}")


print()

print("Fiber Loss:")

print(f"  Minimum : " f"{np.min(fiber_loss_values):.4f} dB")

print(f"  Maximum : " f"{np.max(fiber_loss_values):.4f} dB")

print(f"  Average : " f"{np.mean(fiber_loss_values):.4f} dB")


print("======================================")
