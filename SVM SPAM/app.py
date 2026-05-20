import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import streamlit as st
import re

# ---------------------------
# Load dataset
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("spam_detection.csv")  # Load your CSV
    df = df[['text', 'label']]  # Only keep text and label
    return df

data = load_data()

# ---------------------------
# Split data into features and labels
# ---------------------------
X = data['text']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------
# TF-IDF vectorization
# ---------------------------
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ---------------------------
# Train Multinomial Naive Bayes model
# ---------------------------
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# ---------------------------
# Evaluate model
# ---------------------------
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

# ---------------------------
# Spam words list (informational only)
# ---------------------------
spam_words = [
    "win", "free", "prize", "claim", "urgent", "gift", "cash",
    "lottery", "offer", "buy", "cheap", "click", "reward", "limited",
    "watch now", "10x", "subscribe", "bonus"
]

# ---------------------------
# Functions to detect and highlight spam words
# ---------------------------
def find_spam_words(message):
    message_lower = message.lower()
    words = re.findall(r'\w+', message_lower)
    spam_positions = {}
    
    # Single words
    for idx, word in enumerate(words, start=1):
        if word in spam_words:
            spam_positions[word] = spam_positions.get(word, []) + [idx]

    # Bigrams
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    for idx, phrase in enumerate(bigrams, start=1):
        if phrase in spam_words:
            spam_positions[phrase] = spam_positions.get(phrase, []) + [idx]

    return spam_positions

def highlight_spam(message, spam_positions):
    highlighted = message
    for word, positions in spam_positions.items():
        highlighted = re.sub(
            fr"(?i)\b{re.escape(word)}\b",
            f"<span style='color:red; font-weight:bold'>{word} (pos: {positions})</span>",
            highlighted
        )
    return highlighted

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("Spam Detection App 📧")
st.write("This app uses a Naive Bayes model for better email spam detection.")
st.write(f"Model Accuracy: **{accuracy*100:.2f}%**")

user_input = st.text_area("Enter a message to check if it's spam:")

if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Please enter a message!")
    else:
        # Vectorize input
        input_vec = vectorizer.transform([user_input])
        prediction = model.predict(input_vec)[0]
        prediction_prob = max(model.predict_proba(input_vec)[0])  # Highest probability

        # Detect spam words (informational)
        spam_positions = find_spam_words(user_input)

        # Set box color
        if prediction == 1:
            result_text = "SPAM"
            box_color = "#ffcccc"  # Red
            text_color = "red"
        else:
            result_text = "NOT SPAM"
            box_color = "#ccffcc"  # Green
            text_color = "green"

        # Display prediction in colored box
        st.markdown(
            f"""
            <div style='background-color:{box_color}; color:{text_color}; 
                        padding:15px; border-radius:10px; font-weight:bold; font-size:20px'>
                Prediction: {result_text} (Probability: {prediction_prob*100:.2f}%)
            </div>
            """,
            unsafe_allow_html=True
        )

        # Highlight spam words in message with positions
        if spam_positions:
            st.write("**Spam Words/Phrases Detected with Positions:**")
            st.markdown(
                highlight_spam(user_input, spam_positions),
                unsafe_allow_html=True
            )
        else:
            st.write("No spam words detected in the message.")
