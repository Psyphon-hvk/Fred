import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ✅ Load synthetic dataset
data = pd.read_csv("ml_model/asthma_data.csv")

# ✅ Define Features & Target
X = data.drop(columns=["asthma"])  # Features
y = data["asthma"]  # Target (0 = No, 1 = Yes)

# ✅ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Scale Features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaler

# ✅ Train Model
model = LogisticRegression(max_iter=500)  # Increased max_iter
model.fit(X_train_scaled, y_train)

# ✅ Evaluate Model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# ✅ Save Model & Scaler
joblib.dump(model, "ml_model/asthma_model.pkl")
joblib.dump(scaler, "ml_model/scaler.pkl")
print("Model & Scaler saved successfully!")
