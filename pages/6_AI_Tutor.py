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
st.caption("Your personal AI-powered learning companion — choose explanation depth and get helpful links.")

# ---------------------------
# CONSTANTS & USAGE LIMIT
# ---------------------------
DAILY_LIMIT = 7     # requests per user per day
### DAILY_LIMIT = 7     # requests per user per day

# ---------------------------
# SESSION STATE (usage counting)
@@ -97,9 +97,9 @@
# ---------------------------
# UI: show remaining requests (live)
# ---------------------------
requests_left = DAILY_LIMIT - st.session_state["usage_count"]
st.info(f"📊 Requests Left Today: {requests_left}/{DAILY_LIMIT}")
st.progress(min(st.session_state["usage_count"]/DAILY_LIMIT, 1.0))
# ####requests_left = DAILY_LIMIT - st.session_state["usage_count"]
# ####st.info(f"📊 Requests Left Today: {requests_left}/{DAILY_LIMIT}")
# #####st.progress(min(st.session_state["usage_count"]/DAILY_LIMIT, 1.0))

# ---------------------------
# User controls
@@ -113,56 +113,56 @@
# ---------------------------
# Guard: usage limit
# ---------------------------
if requests_left <= 0:
    st.error("🚫 Daily limit reached! You can ask more questions tomorrow.")
    st.stop()
# ####if requests_left <= 0:
#     #####st.error("🚫 Daily limit reached! You can ask more questions tomorrow.")
#     #####st.stop()

# ---------------------------
# Core function: call Gemini
# ---------------------------
def get_explanation(topic_text: str, level_choice: str, include_links_flag: bool):
    if not gemini_model:
        return {"error": "Gemini model not initialized."}

    prompt = build_prompt(topic_text, level_choice, request_youtube=include_links_flag)
    try:
        resp = gemini_model.generate_content(prompt)
        raw = resp.text or ""
        links = extract_links(raw)
        return {"text": raw.strip(), "links": links}
    except Exception as e:
        return {"error": str(e)}

# ---------------------------
# Action: Explain
# ---------------------------
if st.button("🧠 Explain Topic"):
    if not topic.strip():
        st.warning("Please enter a topic before clicking 'Explain Topic'.")
    else:
        # increment usage count immediately to avoid race
        st.session_state["usage_count"] += 1
        requests_left = DAILY_LIMIT - st.session_state["usage_count"]

        with st.spinner("📚 Generating explanation..."):
            result = get_explanation(topic, level, include_links)

        if result.get("error"):
            st.error(f"Error generating explanation: {result['error']}")
        else:
            st.markdown("---")
            st.markdown(result["text"])
            st.markdown("---")
            if result["links"]:
                st.subheader("🔗 Links & Videos")
                for u in result["links"]:
                    # show cleaned display
                    st.write(f"- [{u}]({u})")
            st.success(f"✨ Request used! Remaining: {requests_left}/{DAILY_LIMIT}")
            # st.success(f"✨ Request used! Remaining: {requests_left}/{DAILY_LIMIT}")
            st.progress(min(st.session_state["usage_count"]/DAILY_LIMIT, 1.0))

            st.success("✨ Request executed.......")
# ---------------------------
# Footer help
# ---------------------------
st.markdown("<br/><br/>", unsafe_allow_html=True)
st.info("💡 Tip: Use 'ELI5' for quick intuitive understanding, 'Exam' for concise revision notes.")
