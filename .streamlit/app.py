
import streamlit as st
import pandas as pd
import joblib
import json
import hashlib
import hmac
import secrets
import re
from pathlib import Path


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="EduAnalytics",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# 2. PROJECT FOLDER PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

USER_FILE = BASE_DIR / "users.json"
MODEL_FILE = BASE_DIR / "student_model.pkl"

DATASET_CANDIDATES = [
    BASE_DIR / "dataset" / "students.csv",
    BASE_DIR / "students.csv"
]

FEATURE_COLUMNS = [
    "Attendance",
    "Study_Hours",
    "Previous_Score",
    "Assignment_Completion",
    "Sleep_Hours"
]


# ==========================================
# 3. USER AUTHENTICATION FUNCTIONS
# ==========================================

def load_users():
    if USER_FILE.exists():
        try:
            with open(USER_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    return {}


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    ).hex()


def register_user(name, student_id, email, password):
    users = load_users()

    name = name.strip()
    student_id = student_id.strip()
    email = email.strip().lower()

    if not name or not student_id or not email or not password:
        return False, "Please fill in all fields."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Enter a valid email address."

    if email in users:
        return False, "This email is already registered."

    if any(
        user["student_id"].lower() == student_id.lower()
        for user in users.values()
    ):
        return False, "This Student ID is already registered."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    salt = secrets.token_hex(16)

    users[email] = {
        "name": name,
        "student_id": student_id,
        "salt": salt,
        "password_hash": hash_password(password, salt)
    }

    try:
        save_users(users)
    except OSError as error:
        return False, f"Could not save account: {error}"

    return True, "Registration successful! Please log in."


def authenticate_user(email, password):
    users = load_users()
    email = email.strip().lower()

    user = users.get(email)

    if not user:
        return False

    entered_hash = hash_password(password, user["salt"])

    return hmac.compare_digest(
        entered_hash,
        user["password_hash"]
    )


# ==========================================
# 4. CUSTOM CSS
# ==========================================


# ==========================================
# 3. CUSTOM CSS - DESKTOP AND MOBILE
# ==========================================

st.markdown("""
<style>

/* Main application background and text */
.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #F5F7FB !important;
    color: #1F2937 !important;
}

/* Headings */
h1 {
    color: #17365D !important;
    font-weight: 800;
}

h2, h3 {
    color: #24476B !important;
    font-weight: 700;
}

/* Normal text and labels */
.stMarkdown p,
.stMarkdown li,
.stText,
label,
[data-testid="stWidgetLabel"] p {
    color: #263445 !important;
}

/* Input fields */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    border-color: #B8C5D6 !important;
}

/* Input placeholders */
input::placeholder,
textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #263445 !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button,
[data-testid="stFormSubmitButton"] button {
    background-color: #1769AA !important;
    color: #FFFFFF !important;
    border-radius: 8px;
    font-weight: bold;
    border: none;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE5F0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #E8EFF8 !important;
}

/* Login card */
.auth-card {
    background: #FFFFFF !important;
    color: #1F2937 !important;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #DCE5F0;
}

/* Mobile responsive design */
@media screen and (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1.5rem !important;
    }

    h1 {
        font-size: 1.8rem !important;
    }

    h2 {
        font-size: 1.4rem !important;
    }

    .auth-card {
        padding: 15px !important;
    }

    [data-testid="stMetric"] {
        padding: 12px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 5. SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_email" not in st.session_state:
    st.session_state.student_email = ""



# 6. LOGIN AND REGISTRATION PAGE
# ==========================================

if not st.session_state.logged_in:

    st.markdown(
        "<h1 style='text-align:center;'>🎓 EduAnalytics</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Student Performance Analytics Portal"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown(
            "<div class='auth-card'>",
            unsafe_allow_html=True
        )

        login_tab, register_tab = st.tabs(
            ["🔐 Student Login", "📝 Registration"]
        )

        # LOGIN

        with login_tab:

            st.subheader("Welcome Back!")

            with st.form("login_form"):

                login_email = st.text_input("Email Address")

                login_password = st.text_input(
                    "Password",
                    type="password"
                )

                login_button = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

            if login_button:

                if authenticate_user(login_email, login_password):

                    st.session_state.logged_in = True

                    st.session_state.student_email = (
                        login_email.strip().lower()
                    )

                    st.rerun()

                else:
                    st.error("Invalid email or password.")

        # REGISTRATION

        with register_tab:

            st.subheader("Create Student Account")

            with st.form("registration_form"):

                reg_name = st.text_input("Full Name")

                reg_id = st.text_input("Student ID")

                reg_email = st.text_input("Email Address")

                reg_password = st.text_input(
                    "Create Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                register_button = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

            if register_button:

                if reg_password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    success, message = register_user(
                        reg_name,
                        reg_id,
                        reg_email,
                        reg_password
                    )

                    if success:
                        st.success(message)
                    else:
                        st.error(message)

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ==========================================
# 7. GET LOGGED-IN STUDENT
# ==========================================

users = load_users()

current_email = st.session_state.student_email

if current_email not in users:

    st.session_state.logged_in = False
    st.session_state.student_email = ""

    st.rerun()

current_student = users[current_email]


# ==========================================
# 8. LOAD MACHINE LEARNING MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


try:
    model = load_model()

except Exception as error:

    st.error(f"Model loading error: {error}")

    st.write("Expected model location:")

    st.code(str(MODEL_FILE))

    st.stop()


# ==========================================
# 9. SIDEBAR
# ==========================================

st.sidebar.title("🎓 EduAnalytics")

st.sidebar.caption("Student Performance System")

st.sidebar.divider()

st.sidebar.success(
    f"Welcome, {current_student['name']}!"
)

st.sidebar.write(
    f"Student ID: {current_student['student_id']}"
)

st.sidebar.write(current_email)

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.student_email = ""

    st.rerun()

st.sidebar.divider()

st.sidebar.subheader("About EduAnalytics")

st.sidebar.write(
    "Analyze academic details and predict "
    "student examination performance."
)

st.sidebar.info(
    "Powered by Python, Pandas, Scikit-learn "
    "and Machine Learning."
)


# ==========================================
# 10. MAIN DASHBOARD
# ==========================================

st.title("🎓 Student Performance Analytics")

st.write(
    f"Welcome to your dashboard, "
    f"**{current_student['name']}**!"
)

st.write(
    "AI-powered academic performance analysis "
    "and student marks prediction platform."
)

st.divider()


# ==========================================
# 11. STUDENT INPUT FORM
# ==========================================

st.subheader("📝 Enter Student Details")

with st.form("student_form"):

    col1, col2 = st.columns(2)

    with col1:

        attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=85.0
        )

        study_hours = st.number_input(
            "Daily Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=4.0
        )

        previous_score = st.number_input(
            "Previous Exam Marks",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

    with col2:

        assignment = st.number_input(
            "Assignment Completion (%)",
            min_value=0.0,
            max_value=100.0,
            value=90.0
        )

        sleep = st.number_input(
            "Sleep Hours",
            min_value=0.0,
            max_value=24.0,
            value=7.0
        )

    submitted = st.form_submit_button(
        "🚀 Predict Student Marks",
        use_container_width=True
    )


# ==========================================
# 12. PREDICTION AND ANALYTICS
# ==========================================

if submitted:

    try:

        # PREPARE STUDENT INPUT

        student = pd.DataFrame([{
            "Attendance": attendance,
            "Study_Hours": study_hours,
            "Previous_Score": previous_score,
            "Assignment_Completion": assignment,
            "Sleep_Hours": sleep
        }])

        # CHECK MODEL FEATURE NAMES

        if hasattr(model, "feature_names_in_"):

            expected_features = list(model.feature_names_in_)

            missing_features = [
                column for column in expected_features
                if column not in student.columns
            ]

            if missing_features:

                raise ValueError(
                    "The trained model expects different input "
                    f"columns. Missing columns: {missing_features}. "
                    f"Model columns: {expected_features}. "
                    f"Application columns: {list(student.columns)}"
                )

            student = student[expected_features]

        # PREDICT STUDENT MARKS

        prediction = float(model.predict(student)[0])

        prediction = max(0, min(100, prediction))

        # PERFORMANCE CATEGORY

        if prediction >= 85:
            category = "Excellent"

        elif prediction >= 70:
            category = "Good"

        elif prediction >= 50:
            category = "Average"

        else:
            category = "Needs Improvement"

        # LOAD STUDENT DATASET

        dataset_path = next(
            (
                path for path in DATASET_CANDIDATES
                if path.is_file()
            ),
            None
        )

        average_marks = None

        if dataset_path is not None:

            dataset = pd.read_csv(dataset_path)

            if "Final_Score" in dataset.columns:

                average_marks = pd.to_numeric(
                    dataset["Final_Score"],
                    errors="coerce"
                ).mean()

        # DISPLAY DASHBOARD

        st.divider()

        st.header("📊 Student Performance Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Predicted Marks",
            f"{prediction:.2f}/100"
        )

        col2.metric(
            "Performance Category",
            category
        )

        col3.metric(
            "Dataset Average",
            f"{average_marks:.2f}/100"
            if average_marks is not None and pd.notna(average_marks)
            else "Not Available"
        )

        # PERFORMANCE GRAPH

        st.subheader("📈 Performance Comparison")

        if average_marks is not None and pd.notna(average_marks):

            comparison = pd.DataFrame({
                "Category": [
                    "Student Prediction",
                    "Dataset Average"
                ],
                "Marks": [
                    prediction,
                    average_marks
                ]
            })

        else:

            comparison = pd.DataFrame({
                "Category": ["Student Prediction"],
                "Marks": [prediction]
            })

            st.warning(
                "Dataset average is unavailable. "
                "Showing the predicted marks only."
            )

        st.bar_chart(
            comparison,
            x="Category",
            y="Marks",
            y_label="Marks",
            height=350
        )

        # ACADEMIC DETAILS

        st.subheader("📋 Academic Details")

        st.dataframe(
            student,
            use_container_width=True
        )

        # PERSONALIZED RECOMMENDATIONS

        st.subheader("💡 Personalized Study Recommendations")

        recommendations = []

        if attendance < 75:

            recommendations.append(
                "Improve attendance and attend classes regularly."
            )

        if study_hours < 3:

            recommendations.append(
                "Increase daily study hours gradually."
            )

        if previous_score < 60:

            recommendations.append(
                "Revise previous topics and practice more questions."
            )

        if assignment < 70:

            recommendations.append(
                "Complete assignments on time."
            )

        if sleep < 6:

            recommendations.append(
                "Maintain a healthy sleep schedule."
            )

        if not recommendations:

            recommendations.append(
                "Excellent! Keep maintaining your current study habits."
            )

        for recommendation in recommendations:

            st.success(recommendation)

        # DOWNLOAD STUDENT REPORT

        st.subheader("📥 Download Student Report")

        report = student.copy()

        report.insert(
            0,
            "Student_Name",
            current_student["name"]
        )

        report.insert(
            1,
            "Student_ID",
            current_student["student_id"]
        )

        report["Predicted_Final_Marks"] = round(
            prediction, 2
        )

        report["Performance_Category"] = category

        report["Dataset_Average"] = (
            round(float(average_marks), 2)
            if average_marks is not None
            and pd.notna(average_marks)
            else "Not Available"
        )

        csv_data = report.to_csv(index=False)

        st.download_button(
            label="📥 Download Student Report",
            data=csv_data,
            file_name=f"{current_student['student_id']}_report.csv",
            mime="text/csv"
        )

        st.success(
            "Student performance analysis completed successfully!"
        )

        st.caption(
            "Predictions are educational estimates based on "
            "your trained machine learning model."
        )

    except Exception as error:

        st.error(f"Prediction Error: {error}")

        st.info(
            "Please check that your model was trained using "
            "the same input features as this application."
        )


# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "EduAnalytics | Student Performance Prediction "
    "| Python | Pandas | Scikit-learn | Streamlit"
)
