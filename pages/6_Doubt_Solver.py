# pages/6_Doubt_Solver.py
import streamlit as st
import google.generativeai as genai
import pdfplumber
import io
import os
import datetime
from PIL import Image

# ---------------- Tesseract Check ----------------
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except Exception:
    TESSERACT_AVAILABLE = False

# ---------------- Page config ----------------
st.set_page_config(page_title="NexStudy Tutor", page_icon="🤖", layout="wide")
st.markdown("<style>footer{visibility:hidden;} </style>", unsafe_allow_html=True)

# Optional logo
_logo_path = "/mnt/data/A_logo_for_EduNex,_an_AI-powered_smart_study_assis.png"
if os.path.exists(_logo_path):
    st.image(_logo_path, width=150)

st.title("🤖 NexStudy Tutor (Doubt Solver)")
st.caption("Ask a question, upload a PDF or image, and get clear step-by-step explanations.")

# ---------------- Gemini initialization ----------------
@st.cache_resource
def init_gemini():
    key = None
    try:
        key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not key:
        return None

    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        st.error(f"Gemini initialization error: {e}")
        return None

gemini_model = init_gemini()

# ---------------- Session state for chat ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "saved" not in st.session_state:
    st.session_state.saved = []

# ---------------- Helpers ----------------
def extract_text_from_pdf(uploaded_file):
    try:
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting PDF text: {e}")
        return ""

def ocr_image(uploaded_image_bytes):
    if not TESSERACT_AVAILABLE:
        return None
    try:
        img = Image.open(io.BytesIO(uploaded_image_bytes)).convert("RGB")
        return pytesseract.image_to_string(img)
    except Exception as e:
        st.warning(f"OCR failed: {e}")
        return None

def call_gemini(prompt: str, max_output_tokens: int = 1024):
    if gemini_model is None:
        return {"error": "Gemini API key not configured."}
    try:
        resp = gemini_model.generate_content(prompt)
        text = resp.text or ""
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

def append_user_message(text, meta=None):
    st.session_state.messages.append({"role": "user", "text": text, "meta": meta or {}})

def append_assistant_message(text, meta=None):
    st.session_state.messages.append({"role": "assistant", "text": text, "meta": meta or {}})

# ---------------- Layout ----------------
left, right = st.columns([1, 2])

# ---------------- Left Column (Controls) ----------------
with left:
    st.markdown("### ⚙️ Controls")
    st.info("Use the chat on the right to ask doubts. Upload PDFs or images if you like.")
    st.markdown("**Input types**")
    input_choice = st.radio("", ("Text", "PDF + Text", "Image + Text"), index=1)

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.success("Chat cleared.")
        st.rerun()
        
    if st.button("Saved answers"):
        if st.session_state.saved:
            st.write("Saved responses:")
            for i, item in enumerate(st.session_state.saved, 1):
                st.markdown(f"**{i}. {item['title']}** — {item['timestamp']}")
                st.write(item["text"])
        else:
            st.info("No saved answers yet.")

# ---------------- Right Column (Chat) ----------------
with right:
    # CSS to ensure black text on chat bubbles
    st.markdown(
        """
        <style>
        .chat-box { max-height: 64vh; overflow:auto; padding:8px; display:flex; flex-direction:column; gap:12px; }
        .user { 
            align-self:flex-end; 
            background:#DCF8C6; 
            color: #000000; 
            padding:12px; 
            border-radius:12px; 
            max-width:80%; 
        }
        .ai { 
            align-self:flex-start; 
            background:#F1F3F5; 
            color: #000000; 
            padding:12px; 
            border-radius:12px; 
            max-width:80%; 
        }
        </style>
        """, unsafe_allow_html=True)

    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                # Format user message
                user_text = msg['text'].replace('\n', '<br>')
                st.markdown(f"<div class='user'><b>You:</b><br>{user_text}</div>", unsafe_allow_html=True)
            else:
                # Format AI message
                ai_text_display = msg['text'].replace('\n', '<br>')
                st.markdown(f"<div class='ai'><b>NexStudy Tutor:</b><br>{ai_text_display}</div>", unsafe_allow_html=True)
                
                # Buttons for AI response
                cols = st.columns([1,1,1,1,1])
                
                if cols[0].button(f"Explain Simpler 🔍 #{i}", key=f"simpler_{i}"):
                    res = call_gemini(f"Explain this simpler:\n\n{msg['text']}")
                    if not res.get("error"):
                        append_assistant_message(res["text"])
                        st.rerun()
                        
                if cols[1].button(f"Show Steps 🪜 #{i}", key=f"steps_{i}"):
                    res = call_gemini(f"Show step-by-step solution:\n\n{msg['text']}")
                    if not res.get("error"):
                        append_assistant_message(res["text"])
                        st.rerun()

                if cols[2].button(f"Generate Quiz 🎯 #{i}", key=f"quiz_{i}"):
                    res = call_gemini(f"Create 5 MCQs from this:\n\n{msg['text']}")
                    if not res.get("error"):
                        append_assistant_message(res["text"])
                        st.rerun()
                        
                if cols[3].button(f"Flashcards 🧾 #{i}", key=f"flash_{i}"):
                    res = call_gemini(f"Create flashcards from this:\n\n{msg['text']}")
                    if not res.get("error"):
                        append_assistant_message(res["text"])
                        st.rerun()
                        
                if cols[4].button(f"Save 💾 #{i}", key=f"save_{i}"):
                    st.session_state.saved.append({"title": msg["text"][:50]+"...", "text": msg["text"], "timestamp": str(datetime.datetime.now())})
                    st.success("Saved!")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- Input Form ----------------
    with st.form(key="doubt_form", clear_on_submit=False):
        user_input = st.text_area("Ask your doubt:", height=140, key="user_input")
        
        uploaded_pdf = None
        uploaded_image = None
        
        # Handle file uploaders based on radio selection
        if input_choice == "PDF + Text":
            uploaded_pdf = st.file_uploader("Upload PDF (≤10MB):", type=["pdf"])
        elif input_choice == "Image + Text":
            uploaded_image = st.file_uploader("Upload Image:", type=["png","jpg","jpeg"])

        submit = st.form_submit_button("Send")

        if submit:
            content_parts = []
            
            # 1. Process PDF
            if uploaded_pdf:
                pdf_bytes = uploaded_pdf.read()
                pdf_text = extract_text_from_pdf(io.BytesIO(pdf_bytes))
                if pdf_text:
                    content_parts.append("PDF content:\n" + pdf_text)
                else:
                    st.warning("PDF text extraction failed.")
            
            # 2. Process Image
            if uploaded_image:
                img_bytes = uploaded_image.read()
                if TESSERACT_AVAILABLE:
                    ocr_text = ocr_image(img_bytes)
                    if ocr_text:
                        content_parts.append("Image OCR text:\n" + ocr_text)
                    else:
                        st.warning("Image OCR failed.")
                else:
                    st.info("OCR not available.")

            # 3. Process User Text
            if user_input and user_input.strip():
                content_parts.append("User question:\n" + user_input.strip())

            # 4. Final Validation & API Call
            if not content_parts:
                st.warning("Please provide a question or upload a file.")
            else:
                full_text = "\n\n".join(content_parts)
                append_user_message(full_text)

                if gemini_model is None:
                    st.error("Gemini API Key missing.")
                else:
                    with st.spinner("Thinking..."):
                        sys_prompt = """You are NexStudy Tutor. Answer clearly and concisely. 
                        If the user asks for steps, provide them. 
                        Base answers on the uploaded content if present."""
                        
                        final_prompt = f"{sys_prompt}\n\nUser Content:\n{full_text}\n\nAnswer:"
                        
                        res = call_gemini(final_prompt)
                        
                        if res.get("error"):
                            st.error(res["error"])
                        else:
                            append_assistant_message(res["text"])
                            st.rerun()
