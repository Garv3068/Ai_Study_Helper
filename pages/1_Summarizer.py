import streamlit as st
from models.slm_summarizer import SmallSummarizer
import pdfplumber

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Summarizer", page_icon="🧠")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
        body {
            background-color: #0d0d0d;
            color: #e0e0e0;
        }
        .stButton button {
            background-color: #111;
            color: white;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: 500;
            transition: 0.3s ease;
        }
        .stButton button:hover {
            background-color: #1a1a1a;
            border-color: #555;
            color: #00FFAA;
        }
        .stTextArea textarea {
            background-color: #111 !important;
            color: #fff !important;
            border-radius: 8px !important;
            border: 1px solid #333 !important;
        }
        .result-box {
            background-color: #111;
            padding: 1em;
            border-radius: 10px;
            border: 1px solid #333;
            margin-top: 1em;
        }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🧠 AI Study Helper - Smart Summarizer")
st.caption("Powered by your custom **SLM (Small Language Model)** for offline summarization.")

# --- LOAD MODEL ---
@st.cache_resource
def load_summarizer():
    return SmallSummarizer()

summarizer = load_summarizer()

# --- PDF EXTRACTION FUNCTION ---
def extract_text_from_pdf(uploaded_file):
    """Extracts text safely from an uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text.strip()

# --- INPUT SECTION ---
input_type = st.radio("Choose Input Type:", ("📄 Upload PDF", "📝 Paste Text"))

text_data = ""

if input_type == "📄 Upload PDF":
    uploaded_file = st.file_uploader("Upload your study material (PDF, max 10 MB):", type="pdf")
    if uploaded_file:
        text_data = extract_text_from_pdf(uploaded_file)
        if not text_data:
            st.warning("⚠️ Couldn’t extract text from this PDF. Try another file.")
else:
    text_data = st.text_area("Paste your study material here:", height=200, placeholder="Enter or paste your notes/text here...")

# --- SUMMARIZE BUTTON ---
if st.button("✨ Summarize", use_container_width=True):
    if not text_data.strip():
        st.warning("⚠️ Please upload or paste some text first.")
    else:
        with st.spinner("Generating your summary... Please wait ⏳"):
            try:
                summary = summarizer.summarize(text_data)
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader("📘 Summary:")
                st.write(summary)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred during summarization: {e}")

# --- FOOTER ---
st.markdown("""
    ---
    <p style="text-align:center; color:#888; font-size:0.9em;">
        🔹 Built by <b>Garv Goel</b> | AI Study Helper v1.0 | Powered by FLAN-T5 SLM
    </p>
""", unsafe_allow_html=True)

