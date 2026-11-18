
import pandas as pd
import joblib

# Load trained model
model = joblib.load("student_model.pkl")

print("\n================================")
print(" STUDENT PERFORMANCE PREDICTION")
print("================================")

# Get student information
attendance = float(input("Enter attendance percentage: "))
study_hours = float(input("Enter daily study hours: "))
previous_score = float(input("Enter previous exam marks: "))
assignment = float(input("Enter assignment completion percentage: "))
sleep = float(input("Enter sleep hours: "))

# Validate inputs
if not (0 <= attendance <= 100 and
        0 <= study_hours <= 24 and
        0 <= previous_score <= 100 and
        0 <= assignment <= 100 and
        0 <= sleep <= 24):

    print("Please enter valid values!")

else:

    # Prepare input data
    student = pd.DataFrame([{
        "Attendance": attendance,
        "Study_Hours": study_hours,
        "Previous_Score": previous_score,
        "Assignment_Completion": assignment,
        "Sleep_Hours": sleep
    }])

    # Predict marks
    prediction = model.predict(student)

    print("\n================================")
    print(" PREDICTION RESULT")
    print("================================")

    print("Predicted Final Marks:",
          round(prediction[0], 2))

    print("================================")
