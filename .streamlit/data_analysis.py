
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv("dataset/students.csv")

# Display first five records
print("First Five Records:")
print(data.head())

# Dataset information
print("\nDataset Information:")
print(data.info())

# Statistical summary
print("\nStatistical Summary:")
print(data.describe())

# Check missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Attendance distribution
plt.figure(figsize=(8, 5))
sns.histplot(data["Attendance"], bins=10, kde=True)
plt.title("Student Attendance Distribution")
plt.xlabel("Attendance Percentage")
plt.ylabel("Number of Students")
plt.show()

# Study hours vs final score
plt.figure(figsize=(8, 5))
sns.scatterplot(
    x="Study_Hours",
    y="Final_Score",
    data=data
)
plt.title("Study Hours vs Final Score")
plt.show()

# Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    data.corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Student Performance Correlation")
plt.show()
