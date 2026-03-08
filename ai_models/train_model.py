import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Set random seed for reproducibility
np.random.seed(42)

print("Generating synthetic training data...")

# Generate 1000 rows of synthetic data
n_samples = 1000

data = {
    "temperature": np.random.uniform(15, 45, n_samples),
    "humidity": np.random.uniform(30, 90, n_samples),
    "air_pollution": np.random.uniform(50, 400, n_samples),
    "vibration": np.random.uniform(0.1, 5.0, n_samples),
    "crack_width": np.random.uniform(0.0, 3.5, n_samples),
}

df = pd.DataFrame(data)


# Create risk_level labels based on rules
def assign_risk_level(row):
    # High risk (2)
    if (row["temperature"] > 40 or row["air_pollution"] > 300 or 
        row["vibration"] > 3.5 or row["crack_width"] > 2.5):
        return 2
    # Medium risk (1)
    elif (row["temperature"] > 30 or row["air_pollution"] > 200 or 
          row["vibration"] > 2.0 or row["crack_width"] > 1.5):
        return 1
    # Low risk (0)
    else:
        return 0


df["risk_level"] = df.apply(assign_risk_level, axis=1)

print(f"Data generated: {len(df)} samples")
print(f"\nRisk level distribution:")
print(df["risk_level"].value_counts().sort_index().rename({0: "Low", 1: "Medium", 2: "High"}))

# Prepare features and labels
X = df[["temperature", "humidity", "air_pollution", "vibration", "crack_width"]]
y = df["risk_level"]

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Train Random Forest Classifier
print("\n" + "=" * 50)
print("Training Random Forest Classifier...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate Random Forest
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nRandom Forest Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Low", "Medium", "High"]))

# Train Isolation Forest for anomaly detection
print("=" * 50)
print("Training Isolation Forest for anomaly detection...")
iso_model = IsolationForest(contamination=0.1, random_state=42)
iso_model.fit(X)
print("Isolation Forest trained successfully")

# Create output directory if it doesn't exist
os.makedirs("ai_models", exist_ok=True)

# Save models
rf_model_path = "ai_models/rf_model.pkl"
iso_model_path = "ai_models/iso_model.pkl"

joblib.dump(rf_model, rf_model_path)
joblib.dump(iso_model, iso_model_path)

print("\n" + "=" * 50)
print("Models saved successfully:")
print(f"  - Random Forest: {rf_model_path}")
print(f"  - Isolation Forest: {iso_model_path}")
print("=" * 50)
