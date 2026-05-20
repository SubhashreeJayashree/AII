import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # for train-test split
from sklearn.preprocessing import LabelEncoder, StandardScaler # for encoding and scaling
from sklearn.svm import SVC # Support Vector Classifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix # for evaluation
import matplotlib.pyplot as plt     # for plotting
import seaborn as sns # for enhanced plotting

st.set_page_config(page_title="SVM Classifier App", layout="wide")
st.title("🧠 SVM Classifier (Support Vector Machine)")

st.markdown("""
This app allows you to upload a dataset and build an SVM model.
""")

# Upload Dataset
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    target_col = st.sidebar.selectbox("Select Target Column", df.columns)

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Encode categorical features
    for col in X.select_dtypes(include=["object"]).columns:
        X[col] = LabelEncoder().fit_transform(X[col])

    if y.dtype == "object":
        y = LabelEncoder().fit_transform(y)

    # Feature scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train test split
    test_size = st.sidebar.slider("Test Size (%)", 10, 50, 20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size/100, random_state=42
    )

    # Model parameters
    st.sidebar.header("Model Parameters")
    kernel = st.sidebar.selectbox("Kernel", ["linear", "poly", "rbf", "sigmoid"])
    c_value = st.sidebar.slider("C (Regularization)", 0.01, 10.0, 1.0)
    gamma = st.sidebar.selectbox("Gamma", ["scale", "auto"])
    degree = st.sidebar.slider("Degree (for poly)", 2, 5, 3)

    # Train SVM model
    model = SVC(kernel=kernel, C=c_value, gamma=gamma, degree=degree, probability=True)
    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Evaluation
    st.subheader("✅ Model Performance")
    acc = accuracy_score(y_test, y_pred)
    st.metric("Accuracy", f"{acc:.2f}")

    st.text("Classification Report")
    st.text(classification_report(y_test, y_pred))

    # Confusion Matrix
    st.subheader("📉 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)

else:
    st.info("👈 Upload a CSV file to start")
