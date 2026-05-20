import streamlit as st # web app framework
import pandas as pd # data manipulation
import numpy as np # numerical operations

from sklearn.model_selection import train_test_split # train-test split
from sklearn.preprocessing import LabelEncoder, StandardScaler # encoding and scaling
from sklearn.linear_model import ElasticNet # Elastic Net model
from sklearn.metrics import mean_squared_error, r2_score    # evaluation metrics

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="Elastic Net Regression", layout="wide")
st.title("📈 Elastic Net Regression App")

st.markdown("""
This app demonstrates **Elastic Net Regression** using Streamlit.
Upload your CSV file and train the model automatically.
""")

# -----------------------------
# Upload Dataset
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Target Column
    # -----------------------------
    target_column = st.selectbox("Select Target Column", df.columns)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # -----------------------------
    # Encode Categorical Features
    # -----------------------------
    for col in X.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

    if y.dtype == "object":
        y = LabelEncoder().fit_transform(y)

    # -----------------------------
    # Feature Scaling
    # -----------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # -----------------------------
    # Train-Test Split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # -----------------------------
    # Model Parameters
    # -----------------------------
    st.sidebar.header("Model Parameters")
    alpha = st.sidebar.slider("Alpha (Regularization strength)", 0.01, 1.0, 0.1)
    l1_ratio = st.sidebar.slider("L1 Ratio (Elastic Net mixing)", 0.0, 1.0, 0.5)

    # -----------------------------
    # Train Elastic Net Model
    # -----------------------------
    model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    model.fit(X_train, y_train)

    # -----------------------------
    # Predictions
    # -----------------------------
    y_pred = model.predict(X_test)

    # -----------------------------
    # Evaluation
    # -----------------------------
    st.subheader("✅ Model Performance")

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.metric("Mean Squared Error (MSE)", f"{mse:.2f}")
    st.metric("R² Score", f"{r2:.2f}")

    st.subheader("📌 Sample Predictions")
    result_df = pd.DataFrame({
        "Actual": y_test,
        "Predicted": y_pred
    }).reset_index(drop=True)

    st.dataframe(result_df.head(10))

else:
    st.info("👈 Upload a CSV file to start training")
