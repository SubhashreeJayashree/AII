# -----------------------------------
# IMPORT LIBRARIES
# -----------------------------------
import streamlit as st
import fitz  # PyMuPDF
import pickle
import pandas as pd
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# -----------------------------------
# STREAMLIT PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="AI Newspaper Classifier", layout="wide")
st.title("📰 AI Newspaper News Classifier")

# -----------------------------------
# TEXT CLEANING
# -----------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------------
# TRAIN MODEL IF NOT EXISTS
# -----------------------------------
if not os.path.exists("model.pkl"):
    st.warning("⚠️ Training model automatically...")

    data = {
        "text": [
            # SPORTS
            "India won the cricket match by six wickets",
            "Football world cup final was thrilling",
            "Tennis championship ends with surprise winner",
            "IPL season begins with opening ceremony",

            # WORLD
            "United Nations discusses global peace issues",
            "War situation escalates in eastern Europe",
            "Diplomatic talks held between countries",
            "Global summit focuses on climate change",

            # EDUCATION
            "New education policy announced by government",
            "Universities introduce artificial intelligence courses",
            "Online learning platforms gain popularity",
            "Students appear for national level exams",

            # BUSINESS
            "Stock market reaches record high today",
            "Investors react to inflation report",
            "Company reports strong quarterly earnings",
            "Startup raises funding from venture capital",

            # TECHNOLOGY
            "Latest technology trends in artificial intelligence",
            "New smartphone launched with advanced features",
            "Cybersecurity threats increase worldwide",
            "Software companies adopt cloud computing"
        ],
        "category": [
            "Sports","Sports","Sports","Sports",
            "World","World","World","World",
            "Education","Education","Education","Education",
            "Business","Business","Business","Business",
            "Technology","Technology","Technology","Technology"
        ]
    }

    df_train = pd.DataFrame(data)
    df_train["text"] = df_train["text"].apply(clean_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )

    X_train = vectorizer.fit_transform(df_train["text"])

    model = MultinomialNB()
    model.fit(X_train, df_train["category"])

    pickle.dump(model, open("model.pkl", "wb"))
    pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

    st.success("✅ Model trained and saved")
else:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -----------------------------------
# PDF UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Newspaper PDF (Text-based)",
    type=["pdf"]
)

# -----------------------------------
# PDF FUNCTIONS
# -----------------------------------
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text().strip()
        if len(text) > 100:
            pages.append(text)
    return pages

def split_news_items(pages):
    news_items = []

    for page in pages:
        # Split by paragraphs or sentence blocks
        chunks = re.split(r'\n{2,}|\.\n', page)

        for chunk in chunks:
            chunk = chunk.strip()
            if 80 <= len(chunk) <= 800:
                news_items.append(chunk)

    return news_items

# -----------------------------------
# PROCESS PDF
# -----------------------------------
if uploaded_file:
    pages = extract_text_from_pdf(uploaded_file)
    news_items = split_news_items(pages)

    st.success(f"🧾 News items detected: {len(news_items)}")

    results = []

    for news in news_items:
        clean_news = clean_text(news)
        vector = vectorizer.transform([clean_news])
        category = model.predict(vector)[0]

        results.append({
            "Category": category,
            "News": news
        })

    df = pd.DataFrame(results)

    # -----------------------------------
    # DISPLAY RESULTS
    # -----------------------------------
    if df.empty:
        st.error("❌ No news detected. Try another PDF.")
    else:
        for cat in sorted(df["Category"].unique()):
            st.subheader(f"🗂️ {cat} News")
            cat_news = df[df["Category"] == cat]

            for i, row in cat_news.iterrows():
                with st.expander(f"📰 {cat} News {i+1}"):
                    st.write(row["News"])

        st.subheader("📊 News Category Distribution")
        st.bar_chart(df["Category"].value_counts())
