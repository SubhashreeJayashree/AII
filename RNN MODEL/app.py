import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout
from tensorflow.keras.optimizers import Adam

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="RNN Model", layout="wide")
st.title("🧠 RNN – Small Dataset Safe Version")

# -----------------------------
# Upload CSV
# -----------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is None:
    st.info("Upload a CSV file to get started")
    st.stop()

df = pd.read_csv(uploaded_file)

st.subheader("Dataset Preview")
st.dataframe(df)

# -----------------------------
# Target selection
# -----------------------------
target = st.sidebar.selectbox("Target column", df.columns)

X = df.drop(columns=[target])
y = df[target]

# -----------------------------
# Encode categorical features
# -----------------------------
for col in X.select_dtypes(include="object"):
    X[col] = LabelEncoder().fit_transform(X[col])

y_encoder = LabelEncoder()
y = y_encoder.fit_transform(y)
num_classes = len(np.unique(y))

# -----------------------------
# Dataset sanity checks
# -----------------------------
if num_classes < 2:
    st.error("❌ Target column must have at least 2 classes")
    st.stop()

if num_classes > len(df) * 0.6:
    st.warning(
        "⚠️ Too many unique classes.\n"
        "This target may not be suitable for classification."
    )

# -----------------------------
# Scale + reshape for RNN
# -----------------------------
X = StandardScaler().fit_transform(X)
X = X.reshape(X.shape[0], X.shape[1], 1)

# -----------------------------
# Safe train-test split
# -----------------------------
test_size = 0.3 if len(X) < 30 else 0.2
class_counts = np.bincount(y)

if np.min(class_counts) < 2:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42
    )
    st.warning("⚠️ Stratified split disabled (rare classes detected)")
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y
    )

# -----------------------------
# Build RNN model
# -----------------------------
model = Sequential()
model.add(SimpleRNN(32, input_shape=(X.shape[1], 1)))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation="softmax"))

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# -----------------------------
# Train model
# -----------------------------
with st.spinner("Training model..."):
    model.fit(
        X_train,
        y_train,
        epochs=30,
        batch_size=8,
        verbose=0
    )

# -----------------------------
# Predict
# -----------------------------
y_pred = np.argmax(model.predict(X_test), axis=1)

# -----------------------------
# Metrics
# -----------------------------
st.metric("Accuracy", accuracy_score(y_test, y_pred))

st.subheader("Classification Report")
st.text(classification_report(y_test, y_pred, zero_division=0))

# -----------------------------
# Confusion Matrix
# -----------------------------
fig, ax = plt.subplots()
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
st.pyplot(fig)
