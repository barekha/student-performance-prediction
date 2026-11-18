
import pandas as pd
import numpy as np
import os

# Generate sample student data
np.random.seed(42)

n = 500

attendance = np.random.randint(40, 101, n)
study_hours = np.random.randint(1, 9, n)
previous_score = np.random.randint(30, 101, n)
assignment_completion = np.random.randint(30, 101, n)
sleep_hours = np.random.randint(4, 10, n)

# Generate final marks for demonstration
final_score = (
    0.25 * attendance
    + 0.15 * study_hours * 10
    + 0.35 * previous_score
    + 0.20 * assignment_completion
    + 0.05 * sleep_hours * 10
    + np.random.normal(0, 5, n)
)

final_score = np.clip(final_score, 0, 100)

# Create DataFrame
data = pd.DataFrame({
    "Attendance": attendance,
    "Study_Hours": study_hours,
    "Previous_Score": previous_score,
    "Assignment_Completion": assignment_completion,
    "Sleep_Hours": sleep_hours,
    "Final_Score": final_score.round(2)
})

# Save dataset
# Automatically create dataset folder
os.makedirs("dataset", exist_ok=True)

# Save CSV file
data.to_csv("dataset/students.csv", index=False)

print("Dataset created successfully!")
print(data.head())
print("Dataset Shape:", data.shape)
