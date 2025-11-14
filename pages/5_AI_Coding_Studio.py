import streamlit as st
import google.generativeai as genai
# from openai import OpenAI
import re
import random

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

   # --------------------------------------------------------------------
# TAB 2 — AI DEBUGGER (with Auto Fix + Explanation)
# --------------------------------------------------------------------
with tab2:
    st.subheader("🧠 Smart Debugger — Find and Fix Your Code")

    lang = st.selectbox("Select Language to Debug", ["Python", "HTML", "CSS", "JavaScript"])
    buggy_code = st.text_area("Paste your code here to debug:")

    if st.button("🔍 Debug Code"):
        if not buggy_code.strip():
            st.error("Please paste some code first.")
        else:
            st.write("🔍 Analyzing your code...")
            fixed_code = buggy_code
            issues = []
            explanation = []

            # ----------------------------
            # 🐍 PYTHON DEBUGGER
            # ----------------------------
            if lang == "Python":
                try:
                    compile(buggy_code, "<string>", "exec")
                    st.success("✅ No syntax errors found.")
                    if "def" not in buggy_code:
                        issues.append("No function defined.")
                        explanation.append("Adding functions can make your code modular and reusable.")
                    if "print(" not in buggy_code:
                        issues.append("No print statement found.")
                        explanation.append("Add print() to display output.")
                except SyntaxError as e:
                    st.error(f"❌ Syntax Error: {e.msg} at line {e.lineno}")

                    if "unterminated string" in str(e) or "EOL" in str(e):
                        fixed_code = re.sub(r'print\(([^)]*)$', r'print(\1")', buggy_code)
                        issues.append("Unclosed string literal detected.")
                        explanation.append("A missing quote was added to close your string.")
                    elif "invalid syntax" in str(e):
                        fixed_code = buggy_code.replace("print ", "print(").replace("\n", ")\n")
                        issues.append("Likely missing parentheses.")
                        explanation.append("Added parentheses to fix print syntax.")
                    else:
                        explanation.append("Syntax issue found; review your code manually.")

                except Exception as e:
                    st.error(f"⚠️ Runtime Error: {str(e)}")
                    issues.append("Runtime error.")
                    explanation.append("This could be due to undefined variables or imports.")

                if issues:
                    st.warning("⚠️ Issues Found:")
                    for i in issues:
                        st.write("•", i)

                    st.subheader("💡 Explanation")
                    for e in explanation:
                        st.write("-", e)

                if fixed_code != buggy_code:
                    st.subheader("✅ Suggested Fixed Code")
                    st.code(fixed_code, language="python")

            # ----------------------------
            # 🌐 HTML DEBUGGER
            # ----------------------------
            elif lang == "HTML":
                if "<html" not in buggy_code.lower():
                    issues.append("Missing <html> tag.")
                    fixed_code = "<html>\n" + buggy_code + "\n</html>"
                    explanation.append("Added missing <html> wrapper.")
                if "<body" not in buggy_code.lower():
                    issues.append("Missing <body> tag.")
                    fixed_code = fixed_code.replace("</html>", "<body>\n</body>\n</html>")
                    explanation.append("Added missing <body> section.")
                if "<!DOCTYPE" not in buggy_code.lower():
                    fixed_code = "<!DOCTYPE html>\n" + fixed_code
                    issues.append("Added missing <!DOCTYPE html> declaration.")
                    explanation.append("Added doctype to define HTML version.")

                if issues:
                    st.warning("⚠️ Issues Found:")
                    for i in issues:
                        st.write("•", i)
                    st.subheader("✅ Corrected HTML")
                    st.code(fixed_code, language="html")

            # ----------------------------
            # 🎨 CSS DEBUGGER
            # ----------------------------
            elif lang == "CSS":
                if not buggy_code.strip().endswith("}"):
                    fixed_code = buggy_code + "\n}"
                    issues.append("Added missing closing brace '}'.")
                    explanation.append("Every CSS block must end with '}'.")
                if ":" not in buggy_code:
                    issues.append("No property:value pair found.")
                    explanation.append("Use format like `color: red;`.")
                if issues:
                    st.warning("⚠️ Issues Found:")
                    for i in issues:
                        st.write("•", i)
                    st.subheader("✅ Corrected CSS")
                    st.code(fixed_code, language="css")

            # ----------------------------
            # ⚙️ JAVASCRIPT DEBUGGER
            # ----------------------------
            elif lang == "JavaScript":
                if "function" not in buggy_code and "=>" not in buggy_code:
                    issues.append("No function found.")
                    explanation.append("Consider defining a function.")
                if "console.log" not in buggy_code:
                    issues.append("Add console.log() for output.")
                    explanation.append("Use console.log() to print results in JS.")
                if not buggy_code.strip().endswith(";"):
                    fixed_code = buggy_code.strip() + ";"
                    issues.append("Added missing semicolon.")
                    explanation.append("Statements should end with semicolons.")

                if issues:
                    st.warning("⚠️ Issues Found:")
                    for i in issues:
                        st.write("•", i)
                    st.subheader("✅ Corrected JavaScript")
                    st.code(fixed_code, language="javascript")
                    
