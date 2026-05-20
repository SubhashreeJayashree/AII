import streamlit as st  # Streamlit for web app
import pandas as pd # For data manipulation
from statsmodels.tsa.holtwinters import ExponentialSmoothing # Holt-Winters method
import matplotlib.pyplot as plt # For plotting

st.set_page_config(page_title="Time Series Exponential Smoothing", layout="wide")
st.title("📈 Time Series Exponential Smoothing (Holt-Winters)")

# -----------------------------
# Upload Dataset
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Select Columns
    # -----------------------------
    date_col = st.sidebar.selectbox("Select Date Column", df.columns, index=0)
    value_col = st.sidebar.selectbox("Select Value Column", df.columns, index=1)

    # -----------------------------
    # Convert Date Column
    # -----------------------------
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)

    # -----------------------------
    # Model Building
    # -----------------------------
    model = ExponentialSmoothing(df[value_col], trend="add", seasonal=None)
    fit = model.fit()

    # -----------------------------
    # Forecasting
    # -----------------------------
    forecast_steps = st.sidebar.slider("Forecast Steps", 5, 30, 10)
    forecast = fit.forecast(steps=forecast_steps)

    # -----------------------------
    # Plotting
    # -----------------------------
    st.subheader("📈 Time Series Plot")
    st.line_chart(df[value_col])

    st.subheader("🔮 Forecast Plot")
    st.line_chart(forecast)

else:
    st.info("👈 Upload a CSV file to start forecasting")
