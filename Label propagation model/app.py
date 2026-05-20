import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.semi_supervised import LabelPropagation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="Label Propagation - Semi Supervised", layout="wide")
st.title("🔗 Semi-Supervised Learning: Label Propagation")

st.markdown("""
Label Propagation is a **semi-supervised learning algorithm**.
Some labels are hidden (-1) and the model spreads labels through similarity.
""")

# -----------------------------
# Upload Dataset
# -----------------------------
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Target Column
    # -----------------------------
    target_column = st.sidebar.selectbox("Select Target Column", df.columns)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # -----------------------------
    # Encode Features
    # -----------------------------
    X_encoded = X.copy()
    for col in X_encoded.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])

    if y.dtype == "object":
        y = LabelEncoder().fit_transform(y)

    # -----------------------------
    # Feature Scaling (IMPORTANT)
    # -----------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_encoded)

    # -----------------------------
    # Create Semi-Supervised Labels
    # -----------------------------
    st.sidebar.subheader("Unlabeled Data Settings")
    unlabeled_ratio = st.sidebar.slider(
        "Percentage of Unlabeled Data",
        0.1, 0.9, 0.3
    )

    y_semi = y.copy()
    rng = np.random.RandomState(42)
    unlabeled_indices = rng.choice(
        len(y_semi),
        int(len(y_semi) * unlabeled_ratio),
        replace=False
    )
    y_semi.iloc[unlabeled_indices] = -1

    st.write(f"🔍 Unlabeled samples: {(y_semi == -1).sum()}")

    # -----------------------------
    # Train-Test Split (Labeled only)
    # -----------------------------
    labeled_mask = y_semi != -1

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled[labeled_mask],
        y[labeled_mask],
        test_size=0.2,
        random_state=42
    )

    # -----------------------------
    # Model Parameters
    # -----------------------------
    st.sidebar.header("Model Parameters")
    kernel = st.sidebar.selectbox("Kernel Type", ["rbf", "knn"])

    gamma = st.sidebar.slider(
        "Gamma (RBF kernel)",
        1, 50, 20
    )

    n_neighbors = st.sidebar.slider(
        "Number of Neighbors (KNN kernel)",
        3, 20, 7
    )

    # -----------------------------
    # Create Model (FIXED)
    # -----------------------------
    if kernel == "rbf":
        model = LabelPropagation(
            kernel="rbf",
            gamma=gamma
        )
    else:
        model = LabelPropagation(
            kernel="knn",
            n_neighbors=n_neighbors
        )

    # -----------------------------
    # Train Model
    # -----------------------------
    model.fit(X_scaled, y_semi)

    # -----------------------------
    # Predict on Test Data
    # -----------------------------
    y_pred = model.predict(X_test)

    # -----------------------------
    # Evaluation
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
    # Label Distribution After Propagation
    # -----------------------------
    st.subheader("📌 Label Distribution After Propagation")

    final_labels = model.transduction_
    label_df = pd.DataFrame({"Label": final_labels})

    fig2, ax2 = plt.subplots()
    sns.countplot(x="Label", data=label_df, ax=ax2)
    st.pyplot(fig2)

else:
    st.info("👈 Upload a CSV file to start")

