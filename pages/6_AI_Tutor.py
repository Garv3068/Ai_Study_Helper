import streamlit as st
import google.generativeai as genai
import re
import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Tutor | NexStudy",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 NexStudy AI Tutor")
st.caption("Your personal AI-powered learning companion — explain any topic clearly with real web insights.")

# ---------------------------
# CONSTANTS
# ---------------------------
DAILY_LIMIT = 7     # requests per user per day

# ---------------------------
# INITIALIZE SESSION STATE
# ---------------------------
if "usage_count" not in st.session_state:
    st.session_state["usage_count"] = 0

if "last_reset" not in st.session_state:
    st.session_state["last_reset"] = str(datetime.date.today())

# Auto reset daily usage
today = str(datetime.date.today())
if st.session_state["last_reset"] != today:
    st.session_state["usage_count"] = 0
    st.session_state["last_reset"] = today

requests_left = DAILY_LIMIT - st.session_state["usage_count"]

# Display remaining requests
st.info(f"📊 **Requests Left Today: {requests_left}/{DAILY_LIMIT}**")

# ---------------------------
# GEMINI INITIALIZATION
# ---------------------------
@st.cache_resource
def init_gemini():
    try:
        key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=key)

        try:
            return genai.GenerativeModel("gemini-2.5-flash")
        except:
            st.warning("⚠️ Gemini 2.5 Flash not available. Switching to Gemini 2.0 Flash.")
            return genai.GenerativeModel("gemini-2.0-flash")

    except Exception as e:
        st.error(f"Gemini initialization error: {e}")
        return None


gemini_model = init_gemini()

# ---------------------------
# AI TUTOR FUNCTION
# ---------------------------
def get_explanation(topic):
    if not gemini_model:
        return "Gemini model not initialized properly."

    try:
        prompt_text = (
            f"You are an educational AI tutor. Explain the topic '{topic}' "
            "in a clear, simple, and structured way for a beginner. "
            "Provide examples and 2–3 YouTube video links for better understanding."
        )

        response = gemini_model.generate_content(prompt_text)

        if not response or not response.text.strip():
            return "Sorry, I couldn't generate a response. Try again."

        return response.text

    except Exception as e:
        return f"Error generating explanation: {e}"

# ---------------------------
# USER INPUT SECTION
# ---------------------------
st.markdown("### 📘 Ask your AI Tutor")

topic = st.text_input("Enter a topic you want to learn (e.g., Recursion, DBMS, Machine Learning):")

# ---------------------------
# CHECK DAILY LIMIT
# ---------------------------
if requests_left <= 0:
    st.error("🚫 Daily limit reached! You can ask more questions tomorrow.")
    st.stop()

if st.button("🧠 Explain Topic"):
    if topic.strip():
        st.session_state["usage_count"] += 1  # Count this request
        requests_left = DAILY_LIMIT - st.session_state["usage_count"]

        with st.spinner("📚 Generating explanation..."):
            explanation = get_explanation(topic)

        st.markdown("---")
        st.markdown(explanation)
        st.markdown("---")

        st.success(f"✨ Request used! **Remaining: {requests_left}/{DAILY_LIMIT}**")

    else:
        st.warning("Please enter a topic before clicking 'Explain Topic'.")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.info("💡 Tip: Ask conceptual, programming, or technical topics for the best learning experience!")
