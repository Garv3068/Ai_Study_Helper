import streamlit as st
import pdfplumber
import nltk
import re, string

nltk.download('punkt')
nltk.download('punkt_tab')

def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    return text

def summarize_text(text, num_sentences=3):
    from nltk.tokenize import sent_tokenize, word_tokenize
    sentences = sent_tokenize(text)
    words = word_tokenize(clean_text(text))
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    ranked = sorted(
        [(sum(freq.get(w.lower(), 0) for w in word_tokenize(s)), s) for s in sentences],
        reverse=True
    )
    return " ".join([s for _, s in ranked[:num_sentences]])

st.title("📝 Smart PDF & Text Summarizer")

input_type = st.radio("Choose Input Type:", ("Upload PDF", "Paste Text"))
text_data = ""

if input_type == "Upload PDF":
    file = st.file_uploader("Upload a PDF", type="pdf")
    if file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_data += page.extract_text() or ""
else:
    text_data = st.text_area("Paste your text here:")

if st.button("Summarize"):
    if text_data.strip():
        st.subheader("📄 Summary:")
        st.write(summarize_text(text_data))
    else:
        st.warning("Please upload or enter text.")
