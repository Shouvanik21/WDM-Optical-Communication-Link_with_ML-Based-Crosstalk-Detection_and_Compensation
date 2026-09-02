import joblib
import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_FILE = BASE_DIR / "ml" / "wdm_dataset.csv"

MODEL_FILE = BASE_DIR / "ml" / "wdm_crosstalk_model.pkl"


# ==========================================
# FEATURES
# ==========================================

FEATURES = [
    "snr_db",
    "received_power",
    "noise_level",
    "fiber_loss_db",
    "dispersion_ps",
    "average_crosstalk",
    "crosstalk_db",
    "ber",
]

TARGET = "severity"


# ==========================================
# LOAD DATASET
# ==========================================

print()

print("==========================================")

print("          TRAINING WDM ML MODEL")

print("==========================================")


if not DATASET_FILE.exists():

    print()

    print("ERROR: Dataset not found.")

    print()

    print("Generate the dataset first:")

    print("python -m ml.dataset_generator")

    raise SystemExit


df = pd.read_csv(DATASET_FILE)


# ==========================================
# BASIC VALIDATION
# ==========================================

required_columns = FEATURES + [
    "severity",
    "label",
]


missing_columns = [column for column in required_columns if column not in df.columns]


if missing_columns:

    print()

    print("ERROR: Missing columns:")

    for column in missing_columns:

        print(f" - {column}")

    raise SystemExit


print()

print(
    "Dataset shape:",
    df.shape,
)


# ==========================================
# CLASS DISTRIBUTION
# ==========================================

print()

print("Class distribution:")


class_names = {
    0: "NORMAL",
    1: "WARNING",
    2: "CRITICAL",
}


for class_id, class_name in class_names.items():

    count = int((df["severity"] == class_id).sum())

    print(f"{class_name:10s}: {count}")


# ==========================================
# FEATURE SUMMARY
# ==========================================

print()

print("Feature ranges:")

print("------------------------------------------")


for feature in FEATURES:

    minimum = df[feature].min()

    maximum = df[feature].max()

    print(f"{feature:20s} " f"{minimum:.8g} -> " f"{maximum:.8g}")


# ==========================================
# INPUT / OUTPUT
# ==========================================

X = df[FEATURES]

y = df[TARGET]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


# ==========================================
# RANDOM FOREST
# ==========================================

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=14,
    min_samples_split=4,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)


# ==========================================
# TRAIN
# ==========================================

print()

print("Training model...")


model.fit(
    X_train,
    y_train,
)


# ==========================================
# TEST
# ==========================================

predictions = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    predictions,
)


# ==========================================
# RESULTS
# ==========================================

print()

print("==========================================")

print("             MODEL RESULTS")

print("==========================================")


print(f"Accuracy: " f"{accuracy * 100:.2f}%")


print()

print(
    classification_report(
        y_test,
        predictions,
        labels=[
            0,
            1,
            2,
        ],
        target_names=[
            "NORMAL",
            "WARNING",
            "CRITICAL",
        ],
        zero_division=0,
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print("Confusion Matrix:")


matrix = confusion_matrix(
    y_test,
    predictions,
    labels=[
        0,
        1,
        2,
    ],
)


print(matrix)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print()

print("Feature Importance:")

print("------------------------------------------")


importance = pd.DataFrame(
    {
        "feature": FEATURES,
        "importance": model.feature_importances_,
    }
)


importance = importance.sort_values(
    by="importance",
    ascending=False,
)


for _, row in importance.iterrows():

    print(f"{row['feature']:20s} " f"{row['importance']:.4f}")


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    MODEL_FILE,
)


print()

print("==========================================")

print("           MODEL SAVED")

print("==========================================")

print()

print(
    "Model:",
    MODEL_FILE,
)

print()

print("Training completed.")
