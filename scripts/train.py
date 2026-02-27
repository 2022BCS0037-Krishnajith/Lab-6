import pandas as pd
import json
import os
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Ensure output directory exists
os.makedirs("app/artifacts", exist_ok=True)

# 1️⃣ Load the dataset
data = pd.read_csv("dataset/winequality.csv", sep=";")

# 2️⃣ Feature selection
X = data.drop("quality", axis=1)
y = data["quality"]

# 3️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4️⃣ Create and fit scaler
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5️⃣ Train the model (Random Forest Regression)
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)

# 6️⃣ Predictions
y_pred = model.predict(X_test_scaled)

# 7️⃣ Evaluation metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse}")
print(f"R2 Score: {r2}")

# 8️⃣ Save trained model and scaler
joblib.dump(model, "app/artifacts/model.pkl")
joblib.dump(scaler, "app/artifacts/scaler.pkl")

print("Model and scaler saved successfully!")

# 9️⃣ Save evaluation metrics
results = {
    "MSE": mse,
    "R2": r2
}

with open("app/artifacts/metrics.json", "w") as f:
    json.dump(results, f, indent=4)