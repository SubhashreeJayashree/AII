#import library for heuritcs ai module app for python with groq and longchain with 
# streamlit
import streamlit as st
from groq import Groq
# from langchain_groq import ChatGroq # Alternative for LangChain
import os
from dotenv import load_dotenv
#how to download groq api
GROQ_API_KEY="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"
client = Groq(api_key=GROQ_API_KEY)
CURRENT_MODEL = "llama-3.3-70b-versatile"
# create a functions for heuristic model(LOGIC GATE)
def heuristic_decision_layer(input_text):
    """
    Simple heuristic: Approves if input is not too short and lacks banned words.
    Returns: (decision, reason)
    """
    banned_words = ["spam", "malicious", "bot"]
    
    if len(input_text) < 10:
        return "REJECTED", "Input too short."
    
    if any(word in input_text.lower() for word in banned_words):
        return "REJECTED", "Contains inappropriate content."
        
    return "APPROVED", "Passes heuristic check."

def forward_to_llama(prompt):
    """
    Forwards input to llama-3.3-70b-versatile.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error calling Llama: {e}"
    # --- Streamlit UI Configuration ---
st.set_page_config(page_title="🛍️ E-Commerce AI Assistant", layout="centered")
st.title("🛍️ E-Commerce AI Assistant")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
if prompt := st.chat_input("Ask about products or your order..."):
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Apply heuristic logic
    decision, reason = heuristic_decision_layer(prompt)
    
    if decision == "REJECTED":
        response = f"*Heuristic Layer Action:* {reason} Your request was blocked and not sent to the AI model."
    else:
        with st.spinner("Thinking..."):
            response = forward_to_llama(prompt)

    # Display assistant response in chat
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Append to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

# Optional: Add a "Clear Chat" button in the sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        st.rerun() # Rerun the script to clear the display