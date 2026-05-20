# ai_detector_app.py
# Run with: streamlit run ai_detector_app.py

# --------------------------
# IMPORTS
# --------------------------
import streamlit as st  # Streamlit library for building web apps
from transformers import AutoTokenizer, AutoModelForSequenceClassification  # Pre-trained models
import torch  # PyTorch for tensor computations
from torch.nn.functional import softmax  # Softmax to convert logits to probabilities

# --------------------------
# STREAMLIT APP CONFIG
# --------------------------
st.set_page_config(page_title="AI vs Human Text Detector")  # Set title of the web page
st.title("AI vs Human Text Detector")  # Display main title in app
st.write("Enter text below to check if it's AI-generated or human-written:")  # Instruction text

# --------------------------
# USER INPUT
# --------------------------
# Text area for user to input text
user_input = st.text_area("Enter your text here:")

# --------------------------
# LOAD MODEL (CACHED)
# --------------------------
@st.cache_resource(show_spinner=True)  # Cache the model so it's not reloaded every time
def load_model():
    """
    Load a pre-trained AI text detector model from Hugging Face.
    Returns:
        tokenizer: converts text into token IDs for the model
        model: pre-trained classification model
    """
    model_name = "roberta-base-openai-detector"  # Pre-trained AI detection model
    tokenizer = AutoTokenizer.from_pretrained(model_name)  # Load tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)  # Load model
    return tokenizer, model

tokenizer, model = load_model()  # Load model and tokenizer

# --------------------------
# PREDICTION FUNCTION
# --------------------------
def predict_ai_text(text):
    """
    Predicts whether the input text is AI-generated or human-written.
    
    Args:
        text (str): The text to classify.
    
    Returns:
        str: Prediction string with confidence.
    """
    # Tokenize the input text for the model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    # Run the model on the tokenized text
    outputs = model(**inputs)

    # Convert model output logits to probabilities
    probs = softmax(outputs.logits, dim=1)
    ai_prob = probs[0][1].item()  # Probability that text is AI-generated
    human_prob = probs[0][0].item()  # Probability that text is human-written

    # Compare probabilities and return readable result
    if ai_prob > human_prob:
        return f"AI-generated text ({ai_prob*100:.2f}% confidence)"
    else:
        return f"Human-generated text ({human_prob*100:.2f}% confidence)"

# --------------------------
# DISPLAY PREDICTION
# --------------------------
if user_input:  # If the user has entered text
    result = predict_ai_text(user_input)  # Get prediction
    st.subheader("Prediction:")  # Display a subheader
    st.write(result)  # Show the result
