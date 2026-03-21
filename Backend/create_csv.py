import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# -----------------------------
# Number of samples
# -----------------------------
n_samples = 500

# -----------------------------
# Sensor ranges (realistic raw values)
# -----------------------------
raw_acetone_range = [0.2, 3.0]   # MQ-3 raw values
raw_ammonia_range = [0.1, 4.5]   # MQ-135 raw values
sgp_range = [0, 150]             # VOC index
temp_range = [20, 40]            # Temperature °C
hum_range = [30, 70]             # Humidity %

# -----------------------------
# Baseline Calibration
# -----------------------------
BASELINE_ACETONE = 0.9
BASELINE_AMMONIA = 1.8

# -----------------------------
# Generate raw sensor data
# -----------------------------
np.random.seed(42)
raw_acetone = np.round(np.random.uniform(*raw_acetone_range, n_samples), 6)
raw_ammonia = np.round(np.random.uniform(*raw_ammonia_range, n_samples), 6)
sgp = np.round(np.random.uniform(*sgp_range, n_samples), 1)
temp = np.round(np.random.uniform(*temp_range, n_samples), 1)
hum = np.round(np.random.uniform(*hum_range, n_samples), 1)

# -----------------------------
# Calibrate sensors
# -----------------------------
corrected_acetone = np.round(raw_acetone - BASELINE_ACETONE, 3)
corrected_ammonia = np.round(raw_ammonia - BASELINE_AMMONIA, 3)

# -----------------------------
# Generate labels based on app.py rules
# -----------------------------
diabetes_stage = [
    "Normal" if a < 1.0 else "Mild" if 1.0 <= a < 2.5 else "Severe"
    for a in corrected_acetone
]

kidney_stage = [
    "Normal" if a < 2.0 else "Mild" if 2.0 <= a < 4.0 else "Severe"
    for a in corrected_ammonia
]

hydration_status = [
    "Hydrated" if (h >= 45 and a < 2.0 and b < 3.0) else "Dehydrated"
    for h, a, b in zip(hum, corrected_acetone, corrected_ammonia)
]

# -----------------------------
# Generate timestamps
# -----------------------------
start_time = datetime.now()
timestamps = [(start_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(n_samples)]

# -----------------------------
# Create DataFrame with same columns
# -----------------------------
df = pd.DataFrame({
    "timestamp": timestamps,
    "raw_acetone": raw_acetone,
    "raw_ammonia": raw_ammonia,
    "corrected_acetone": corrected_acetone,
    "corrected_ammonia": corrected_ammonia,
    "temperature": temp,
    "humidity": hum,
    "voc_index": sgp,
    "voc_type": ["Endogenous"]*n_samples,  # default placeholder
    "diabetes_stage": diabetes_stage,
    "kidney_stage": kidney_stage,
    "hydration_status": hydration_status
})

# -----------------------------
# Save CSV
# -----------------------------
folder_path = r"C:\Breath_Invasive\Backend\data"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "sensor_data.csv")
df.to_csv(file_path, index=False)

print(f"✅ CSV created successfully with {n_samples} rows at: {file_path}")
print(df.head())