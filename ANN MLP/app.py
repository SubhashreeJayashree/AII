import streamlit as st #streamlit library for building web applications
import pandas as pd #pandas library for data manipulation and analysis
import numpy as np #numpy library for numerical operations

from sklearn.model_selection import train_test_split #sklearn library used in machine learning for splitting datasets into training and testing sets
from sklearn.preprocessing import LabelEncoder, StandardScaler #LabelEncoder converts categorical labels into numerical format, StandardScaler standardizes features by removing the mean and scaling to unit variance
from sklearn.neural_network import MLPClassifier, MLPRegressor #MLPClassifier is used for classification tasks, MLPRegressor is used for regression tasks
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score #accuracy_score measures classification accuracy, mean_squared_error measures average squared difference between predicted and actual values, r2_score indicates proportion of variance explained by the model
# ---------------- Streamlit App ----------------
st.set_page_config(page_title="ANN MLP Toggle", layout="wide")
st.title("🧠 ANN (MLP) App")

# ---------------- Sidebar ----------------
st.sidebar.title("Settings")

task = st.sidebar.selectbox(
    "Select Task",
    ("Classification", "Regression")
)

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# ---------------- Main Area ----------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    target_column = st.selectbox("Select Target Column", df.columns)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # ---------------- Data Preprocessing ----------------
    for col in X.select_dtypes(include=["object"]).columns:
        X[col] = LabelEncoder().fit_transform(X[col])

    if y.dtype == "object":
        y = LabelEncoder().fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # ---------------- Model Training ----------------
    if task == "Regression":
        model = MLPRegressor(max_iter=500, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        st.metric("MSE", f"{mse:.2f}")
        st.metric("R2 Score", f"{r2:.2f}")

    else:  # Classification
        model = MLPClassifier(max_iter=500, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        st.metric("Accuracy", f"{acc:.2f}")

else:
    st.info("👈 Upload a CSV file to start")
