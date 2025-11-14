import streamlit as st
import google.generativeai as genai
from openai import OpenAI

# ----------------------------------
# API KEYS
# ----------------------------------

# Gemini (Code Generator)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# OpenAI (Code Debugger)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------------
# MODELS
# ----------------------------------

gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ----------------------------------
# LANGUAGE OPTIONS
# ----------------------------------

SUPPORTED_LANGUAGES = {
    "Python": "python",
    "HTML": "html",
    "CSS": "css",
    "C": "c",
    "C++": "cpp",
    "Java": "java"
}

# ----------------------------------
# STREAMLIT UI
# ----------------------------------

st.title("🧠 NexStudy – AI Coding Studio")
st.caption("Generate & Debug Code using Gemini + OpenAI")

# Operation Selector
action = st.selectbox(
    "Select Action:",
    ["Generate Code (Gemini)", "Debug Code (OpenAI)"]
)

# Language Selector
language_choice = st.selectbox(
    "Select Programming Language:",
    list(SUPPORTED_LANGUAGES.keys())
)
syntax_highlight = SUPPORTED_LANGUAGES[language_choice]

# Text Input
code_input = st.text_area(
    "Enter your prompt or code here:",
    height=250,
    placeholder="Write your prompt or paste your code here..."
)

# Action Button
if st.button("Run"):
    if not code_input.strip():
        st.warning("Please enter some text or code before running.")
        st.stop()

    # =====================================================
    # 1️⃣ CODE GENERATION USING GEMINI
    # =====================================================
    if action == "Generate Code (Gemini)":
        try:
            with st.spinner(f"Generating {language_choice} code using Gemini…"):
                response = gemini_model.generate_content(
                    f"""
                    Generate clean, well-structured {language_choice} code.
                    Only output valid code.
                    User request/prompt:
                    {code_input}
                    """
                )

            generated_code = response.text
            st.subheader(f"✅ Generated {language_choice} Code (Gemini)")
            st.code(generated_code, language=syntax_highlight)

        except Exception as e:
            st.error(f"Gemini Error: {str(e)}")

    # =====================================================
    # 2️⃣ CODE DEBUGGING USING OPENAI
    # =====================================================
    else:
        try:
            with st.spinner(f"Debugging {language_choice} code using OpenAI…"):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
                            Debug the following {language_choice} code.
                            Fix all errors and return a corrected version only.
                            Code:
                            {code_input}
                            """
                        }
                    ]
                )

            debugged_code = response.choices[0].message.content
            st.subheader(f"🛠️ Debugged {language_choice} Code (OpenAI)")
            st.code(debugged_code, language=syntax_highlight)

        except Exception as e:
            st.error(f"OpenAI Debugger Error: {str(e)}")
