import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="Ranking Algorithm App", layout="wide")
st.title("🏆 Ranking Algorithm using Weighted Scoring")

st.markdown("""
This app ranks items using a **weighted scoring method**.
Upload a dataset and choose the criteria weights.
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
    # Choose Criteria Columns
    # -----------------------------
    st.sidebar.header("Select Criteria Columns")

    # Select multiple columns as criteria
    criteria_cols = st.sidebar.multiselect(
        "Select criteria columns (numeric)",
        df.select_dtypes(include=np.number).columns
    )

    if len(criteria_cols) < 1:
        st.warning("Select at least one numeric column as criteria.")
        st.stop()

    # -----------------------------
    # Input weights for each criterion
    # -----------------------------
    st.sidebar.header("Enter Weights (0-1)")

    weights = {}
    total_weight = 0
    for col in criteria_cols:
        w = st.sidebar.slider(f"Weight for {col}", 0.0, 1.0, 0.5, 0.1)
        weights[col] = w
        total_weight += w

    if total_weight == 0:
        st.warning("Total weight cannot be 0.")
        st.stop()

    # Normalize weights
    for col in weights:
        weights[col] = weights[col] / total_weight

    # -----------------------------
    # Normalize criteria values
    # -----------------------------
    df_norm = df.copy()
    for col in criteria_cols:
        df_norm[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    # -----------------------------
    # Compute weighted score
    # -----------------------------
    df_norm["Weighted Score"] = 0
    for col in criteria_cols:
        df_norm["Weighted Score"] += df_norm[col] * weights[col]

    # -----------------------------
    # Ranking
    # -----------------------------
    df_norm["Rank"] = df_norm["Weighted Score"].rank(ascending=False).astype(int)
    df_norm = df_norm.sort_values("Rank")

    st.subheader("🏅 Ranking Result")
    st.dataframe(df_norm)

    # -----------------------------
    # Plot ranking
    # -----------------------------
    st.subheader("📈 Ranking Chart")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="Rank", y="Weighted Score", data=df_norm, ax=ax)
    ax.set_title("Rank vs Score")
    st.pyplot(fig)

else:
    st.info("👈 Upload a CSV file to start ranking")
