import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
data = pd.read_csv("breath_dataset.csv")

# Features
X = data[["acetone", "ammonia", "voc", "humidity", "temperature"]]

# Label encoders
le_diabetes = LabelEncoder()
le_kidney = LabelEncoder()
le_hydration = LabelEncoder()

y_diabetes = le_diabetes.fit_transform(data["diabetes"])
y_kidney = le_kidney.fit_transform(data["kidney"])
y_hydration = le_hydration.fit_transform(data["hydration"])

# Split dataset
X_train, X_test, y_train_d, y_test_d = train_test_split(X, y_diabetes, test_size=0.2, random_state=42)
_, _, y_train_k, y_test_k = train_test_split(X, y_kidney, test_size=0.2, random_state=42)
_, _, y_train_h, y_test_h = train_test_split(X, y_hydration, test_size=0.2, random_state=42)

# Train models
model_diabetes = RandomForestClassifier(n_estimators=100)
model_kidney = RandomForestClassifier(n_estimators=100)
model_hydration = RandomForestClassifier(n_estimators=100)

model_diabetes.fit(X_train, y_train_d)
model_kidney.fit(X_train, y_train_k)
model_hydration.fit(X_train, y_train_h)

# Predict
pred_d = model_diabetes.predict(X_test)
pred_k = model_kidney.predict(X_test)
pred_h = model_hydration.predict(X_test)

print("Diabetes Accuracy:", accuracy_score(y_test_d, pred_d))
print("Kidney Accuracy:", accuracy_score(y_test_k, pred_k))
print("Hydration Accuracy:", accuracy_score(y_test_h, pred_h))

# Save models
joblib.dump(model_diabetes, "diabetes_model.pkl")
joblib.dump(model_kidney, "kidney_model.pkl")
joblib.dump(model_hydration, "hydration_model.pkl")

joblib.dump(le_diabetes, "le_diabetes.pkl")
joblib.dump(le_kidney, "le_kidney.pkl")
joblib.dump(le_hydration, "le_hydration.pkl")

print("Models saved successfully!")