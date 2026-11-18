
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# Step 1: Load dataset
data = pd.read_csv("dataset/students.csv")

# Step 2: Select input features
X = data[[
    "Attendance",
    "Study_Hours",
    "Previous_Score",
    "Assignment_Completion",
    "Sleep_Hours"
]]

# Step 3: Select target
y = data["Final_Score"]

# Step 4: Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 5: Create model
model = LinearRegression()

# Step 6: Train model
model.fit(X_train, y_train)

# Step 7: Save model
joblib.dump(model, "student_model.pkl")

print("MODEL TRAINING COMPLETED")
print("Model saved successfully!")

# Step 8: Predictions
y_pred = model.predict(X_test)

# Step 9: Evaluation
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Step 10: New student prediction
new_student = pd.DataFrame([{
    "Attendance": 85,
    "Study_Hours": 4,
    "Previous_Score": 75,
    "Assignment_Completion": 90,
    "Sleep_Hours": 7
}])

prediction = model.predict(new_student)

print("Predicted Final Marks:", round(prediction[0], 2))
