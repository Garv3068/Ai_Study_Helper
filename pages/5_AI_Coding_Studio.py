import streamlit as st
import re
import random
import google.generativeai as genai   # ✅ Added for Gemini

st.set_page_config(page_title="AI Coding Studio", page_icon="💻")

# ------------------------------------------------------------
# ✅ GEMINI INITIALIZATION ADDED (Required for Debugger)
# ------------------------------------------------------------
@st.cache_resource
def init_gemini():
    try:
        key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=key)
        try:
            return genai.GenerativeModel("gemini-2.5-flash-lite")
        except Exception:
            st.warning("⚠️ Gemini 2.5 Flash not available. Switching to Gemini 2.0 Flash.")
            return genai.GenerativeModel("gemini-2.0-flash-lite")
    except Exception as e:
        st.error(f"Gemini initialization error: {e}")
        return None

gemini_model = init_gemini()
# ------------------------------------------------------------
# PAGE TITLE + TABS
# ------------------------------------------------------------
st.title("💻 AI Coding Studio")
st.caption("Generate, debug, and learn to code — all in one place!")

tab1, tab2 = st.tabs(["⚙️ Code Generator", "🧠 Smart Debugger"])

# ------------------------------------------------------------
# TAB 1 — GEMINI-ONLY CODE GENERATOR (NO RULE BASED)
# ------------------------------------------------------------
with tab1:
    st.subheader("⚙️ Code Generator")

    lang = st.selectbox("Select Language", ["Python", "HTML", "CSS", "JavaScript"])
    prompt = st.text_area("Describe what you want to build:")

    if st.button("🚀 Generate Code"):
        if not prompt.strip():
            st.error("Please enter a prompt first.")
            st.stop()

        if gemini_model is None:
            st.error("Gemini model not initialized.")
            st.stop()

        with st.spinner("✨ Using Gemini to generate code..."):
            try:
                ai_prompt = f"""
                You are an expert {lang} developer.

                Generate fully working, clean and optimized code for:
                "{prompt}"

                MUST FOLLOW:
                - Only output code
                - No explanation text
                - No markdown fences except codeblocks if required

                Language: {lang}
                """

                response = gemini_model.generate_content(ai_prompt)

                code_result = response.text.strip() if response.text else "No code generated."

                st.success(f"✅ Generated {lang} code below:")
                st.code(code_result, language=lang.lower())

            except Exception as e:
                st.error(f"Gemini Code Generation Error: {e}")

# ------------------------------------------------------------
# TAB 2 — GEMINI-POWERED DEBUGGER
# ------------------------------------------------------------
with tab2:
    st.subheader("🛠️ AI Debugger")

    debug_lang = st.selectbox(
        "Select Language to Debug",
        ["Python", "HTML", "CSS", "JavaScript", "C", "C++", "Java"]
    )

    buggy_code = st.text_area(
        "Paste your buggy code:",
        height=250,
        placeholder="Paste your code here…"
    )

    if st.button("Debug Code"):

        if not buggy_code.strip():
            st.error("❌ Please paste some code to debug.")
            st.stop()

        if gemini_model is None:
            st.error("Gemini model not initialized.")
            st.stop()

        with st.spinner("🔍Debugging Code......."):
            try:
                prompt = f"""
                You are an expert {debug_lang} programmer and debugger.

                TASK:
                - Detect all syntax and logical errors.
                - Explain every issue in simple terms.
                - Provide a fully corrected version of the code.
                - Provide best practices.

                FORMAT STRICTLY:
                ### Issues Found:
                - issue 1
                - issue 2

                ### Explanation:
                explanation text...

                ### Fixed Code:
                ```{debug_lang.lower()}
                corrected code here
                ```

                ### Best Practices:
                - tip 1
                - tip 2

                --- CODE BEGIN ---
                {buggy_code}
                --- CODE END ---
                """

                response = gemini_model.generate_content(prompt)

                st.subheader("🔍 Debugging Report")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Gemini Debugger Error: {str(e)}")
