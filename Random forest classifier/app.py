import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# Streamlit App Configuration
# -----------------------------
st.set_page_config(page_title="Random Forest Classifier", layout="wide")
st.title("🌳 Random Forest Classifier with Streamlit")

# -----------------------------
# Upload Dataset
# -----------------------------
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Target Column Selection
    # -----------------------------
    target_column = st.sidebar.selectbox(
        "Select Target Column",
        df.columns
    )

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # -----------------------------
    # Encode Categorical Features
    # -----------------------------
    X_encoded = X.copy()
    for col in X_encoded.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])

    if y.dtype == "object":
        y = LabelEncoder().fit_transform(y)

    # -----------------------------
    # Train-Test Split
    # -----------------------------
    test_size = st.sidebar.slider("Test Size", 0.1, 0.5, 0.2)
    random_state = st.sidebar.number_input("Random State", value=42)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=test_size, random_state=random_state
    )

    # -----------------------------
    # Random Forest Hyperparameters
    # -----------------------------
    st.sidebar.header("Model Parameters")
    n_estimators = st.sidebar.slider("Number of Trees", 50, 500, 100)
    max_depth = st.sidebar.slider("Max Depth", 2, 50, 10)
    min_samples_split = st.sidebar.slider("Min Samples Split", 2, 10, 2)

    # -----------------------------
    # Train Model
    # -----------------------------
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # -----------------------------
    # Evaluation Metrics
    # -----------------------------
    st.subheader("✅ Model Performance")

    accuracy = accuracy_score(y_test, y_pred)
    st.metric("Accuracy", f"{accuracy:.2f}")

    st.text("Classification Report")
    st.text(classification_report(y_test, y_pred))

    # -----------------------------
    # Confusion Matrix
    # -----------------------------
    st.subheader("📉 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    st.pyplot(fig)

    # -----------------------------
    # Feature Importance
    # -----------------------------
    st.subheader("⭐ Feature Importance")
    importances = model.feature_importances_
    feature_df = pd.DataFrame({
        "Feature": X_encoded.columns,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    st.dataframe(feature_df)

    fig2, ax2 = plt.subplots()
    sns.barplot(
        data=feature_df,
        x="Importance",
        y="Feature",
        ax=ax2
    )
    st.pyplot(fig2)

else:
    st.info("👈 Upload a CSV file to get started")
