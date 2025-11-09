import streamlit as st
import pdfplumber
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt', quiet=True)

st.title("🗂️ Quick Revision Flashcards")

uploaded_file = st.file_uploader("Upload your notes (PDF)", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = "".join([page.extract_text() or "" for page in pdf.pages])

    sentences = sent_tokenize(text)
    flashcards = [s for s in sentences if len(s.split()) > 5]

    if flashcards:
        index = st.slider("Select flashcard", 1, len(flashcards))
        st.info(flashcards[index - 1])
    else:
        st.warning("Not enough text to generate flashcards.")
else:
    st.caption("Upload a PDF to start creating flashcards!")
