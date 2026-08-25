import csv
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ======================================
# LOAD DATASET
# ======================================

X = []
y = []


with open("wdm_dataset.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        features = [
            float(row["snr"]),
            float(row["received_power"]),
            float(row["noise"]),
            float(row["fiber_loss"]),
            float(row["dispersion"]),
            float(row["average_crosstalk"]),
            float(row["crosstalk_db"]),
            float(row["ber"]),
        ]

        label = int(row["label"])

        X.append(features)

        y.append(label)


# ======================================
# TRAIN / TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)


# ======================================
# RANDOM FOREST
# ======================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1,
)


# ======================================
# TRAIN
# ======================================

model.fit(X_train, y_train)


# ======================================
# PREDICTION
# ======================================

predictions = model.predict(X_test)


# ======================================
# EVALUATION
# ======================================

accuracy = accuracy_score(y_test, predictions)


print()

print("========== MODEL RESULTS ==========")


print(f"Accuracy: {accuracy:.4f}")


print()

print("Classification Report:")


print(
    classification_report(
        y_test,
        predictions,
        target_names=["NORMAL", "WARNING", "CRITICAL"],
        zero_division=0,
    )
)


print()

print("Confusion Matrix:")


print(confusion_matrix(y_test, predictions))


# ======================================
# FEATURE IMPORTANCE
# ======================================

feature_names = [
    "SNR",
    "Received Power",
    "Noise",
    "Fiber Loss",
    "Dispersion",
    "Average Crosstalk",
    "Crosstalk dB",
    "BER",
]


print()

print("========== FEATURE IMPORTANCE ==========")


for name, importance in zip(feature_names, model.feature_importances_):

    print(f"{name:20s}: " f"{importance:.4f}")


# ======================================
# SAVE MODEL
# ======================================

joblib.dump(model, "wdm_crosstalk_model.pkl")


print()

print("Model saved as " "wdm_crosstalk_model.pkl")
