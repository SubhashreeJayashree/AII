# ---------------------------------------------
# Import required libraries
# ---------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# ---------------------------------------------
# Page Configuration
# ---------------------------------------------
st.set_page_config(
    page_title="CART Algorithm App",
    page_icon="🌳",
    layout="wide"
)

# ---------------------------------------------
# App Title and Description
# ---------------------------------------------
st.title("🌳 CART Algorithm Application using Streamlit")
st.write(
    "This app demonstrates the **CART (Classification and Regression Tree)** "
    "algorithm using the Iris dataset."
)

# ---------------------------------------------
# Load Dataset
# ---------------------------------------------
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["target"] = iris.target
df["species"] = df["target"].map(dict(enumerate(iris.target_names)))

# ---------------------------------------------
# Dataset Preview
# ---------------------------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# ---------------------------------------------
# Sidebar Controls
# ---------------------------------------------
st.sidebar.header("⚙️ Model Settings")

max_depth = st.sidebar.slider("Max Tree Depth", 1, 10, 3)
min_samples_split = st.sidebar.slider("Min Samples Split", 2, 10, 2)

# ---------------------------------------------
# Prepare Data
# ---------------------------------------------
X = df[iris.feature_names]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------------------
# Train CART Model
# ---------------------------------------------
model = DecisionTreeClassifier(
    criterion="gini",   # CART uses Gini Index
    max_depth=max_depth,
    min_samples_split=min_samples_split,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------------------------
# Model Evaluation
# ---------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

st.subheader("✅ Model Performance")
st.write(f"**Accuracy:** {accuracy:.2f}")

# ---------------------------------------------
# Confusion Matrix
# ---------------------------------------------
st.subheader("🔍 Confusion Matrix")
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots()
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=iris.target_names,
    yticklabels=iris.target_names
)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
st.pyplot(fig)

# ---------------------------------------------
# Decision Tree Visualization
# ---------------------------------------------
st.subheader("🌳 Decision Tree Visualization")

# 👉 IMPORTANT RECTIFICATION EXPLANATION
st.info(
    "📌 **How to read the tree:**\n\n"
    "- **Left branch = TRUE condition** (feature ≤ threshold)\n"
    "- **Right branch = FALSE condition** (feature > threshold)\n\n"
    "Scikit-learn does not explicitly display TRUE/FALSE on branches, "
    "but this rule applies to every split."
)

fig2, ax2 = plt.subplots(figsize=(16, 8))
plot_tree(
    model,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    ax=ax2
)
st.pyplot(fig2)

# ---------------------------------------------
# User Input Prediction
# ---------------------------------------------
st.subheader("🧪 Make a Prediction")

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.slider("Sepal Length (cm)", 4.0, 8.0, 5.1)
    sepal_width = st.slider("Sepal Width (cm)", 2.0, 4.5, 3.5)

with col2:
    petal_length = st.slider("Petal Length (cm)", 1.0, 7.0, 1.4)
    petal_width = st.slider("Petal Width (cm)", 0.1, 2.5, 0.2)

input_data = np.array([
    [sepal_length, sepal_width, petal_length, petal_width]
])

prediction = model.predict(input_data)
prediction_class = iris.target_names[prediction[0]]

st.success(f"🌼 Predicted Species: **{prediction_class}**")

# ---------------------------------------------
# Final Explanation (Exam Ready)
# ---------------------------------------------
st.subheader("📘 Explanation (For Viva / Exam)")
st.markdown("""
- CART uses **binary splits**
- Each node tests a condition: **feature ≤ threshold**
- **Left child → TRUE**
- **Right child → FALSE**
- The tree stops splitting when nodes become pure or depth limit is reached
""")

# ---------------------------------------------
# Footer
# ---------------------------------------------
st.markdown("---")
st.markdown("Built with ❤️ using **CART Algorithm & Streamlit**")
