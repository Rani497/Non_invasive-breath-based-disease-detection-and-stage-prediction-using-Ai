import pandas as pd
import numpy as np
import random

rows = 300  # number of samples

data = []

for _ in range(rows):

    # Randomly choose health stage
    diabetes_stage = random.choice(["Normal", "Mild", "High Risk"])
    kidney_stage = random.choice(["Normal", "Mild", "High Risk"])

    # Generate Acetone based on diabetes stage
    if diabetes_stage == "Normal":
        acetone = round(np.random.uniform(0.3, 0.9), 2)
    elif diabetes_stage == "Mild":
        acetone = round(np.random.uniform(1.0, 1.8), 2)
    else:
        acetone = round(np.random.uniform(1.9, 3.0), 2)

    # Generate Ammonia based on kidney stage
    if kidney_stage == "Normal":
        ammonia = round(np.random.uniform(0.2, 0.8), 2)
    elif kidney_stage == "Mild":
        ammonia = round(np.random.uniform(0.9, 1.5), 2)
    else:
        ammonia = round(np.random.uniform(1.6, 2.5), 2)

    # VOC random realistic range
    voc = random.randint(100, 250)

    # Humidity
    humidity = random.randint(35, 75)

    # Hydration label based on humidity
    if humidity > 60:
        hydration = "Hydrated"
    elif humidity > 45:
        hydration = "Moderate"
    else:
        hydration = "Dehydrated"

    # Temperature realistic
    temperature = random.randint(28, 35)

    data.append([acetone, ammonia, voc, humidity, temperature,
                 diabetes_stage, kidney_stage, hydration])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "acetone", "ammonia", "voc",
    "humidity", "temperature",
    "diabetes", "kidney", "hydration"
])

# Save to CSV
df.to_csv("breath_dataset.csv", index=False)

print("Dataset generated successfully!")