import streamlit as st
import random

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Learning Dashboard")
st.write("Track your progress and see how much you’ve learned!")

# --- Simulated stats (Phase 1: local/session only) ---
if "quiz_attempts" not in st.session_state:
    st.session_state.quiz_attempts = random.randint(2, 10)
if "average_accuracy" not in st.session_state:
    st.session_state.average_accuracy = random.randint(50, 100)
if "summaries_made" not in st.session_state:
    st.session_state.summaries_made = random.randint(3, 12)
if "flashcards_created" not in st.session_state:
    st.session_state.flashcards_created = random.randint(5, 20)

# --- Display key metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧠 Quizzes Attempted", st.session_state.quiz_attempts)
col2.metric("🎯 Avg Accuracy", f"{st.session_state.average_accuracy}%")
col3.metric("📄 Summaries Made", st.session_state.summaries_made)
col4.metric("🎴 Flashcards Created", st.session_state.flashcards_created)

st.divider()
st.subheader("📈 Progress Overview")

# --- Placeholder for chart (Phase 1: random progress trend) ---
import matplotlib.pyplot as plt

x = list(range(1, 8))
y = [random.randint(40, 100) for _ in x]

plt.figure(figsize=(6, 3))
plt.plot(x, y, marker='o')
plt.title("Weekly Learning Progress")
plt.xlabel("Days")
plt.ylabel("Score (%)")
st.pyplot(plt)

st.info("💡 Tip: In the next update, your real progress will appear here once we add user tracking.")
