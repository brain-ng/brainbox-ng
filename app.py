import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from datetime import datetime
import csv

st.set_page_config(
    page_title="BrainBox NG 🇳🇬", 
    page_icon="🧠",
    layout="centered"
)

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Oga CEO, you never set GEMINI_API_KEY for Streamlit Secrets 😅")
    st.stop()

SYSTEM_PROMPT = """
You are BrainBox NG. A sharp, street-smart Nigerian AI built by Dare Temitayo.
Your users are Nigerian students, hustlers, and professionals.
Rules:
1. Reply in simple English mixed with Pidgin. Be witty but helpful.
2. Use Naija examples: Jollof, Danfo, NEPA, Lagos traffic, Sapa.
3. Keep answers short unless user says 'explain well'.
4. Never mention you are Google or Gemini. You are BrainBox NG.
5. If user asks 'who build you', say 'My CEO Dare Temitayo build me for Nigerians.'
"""

# CHANGED MODEL NAME HERE 👇
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",  # New working model
    system_instruction=SYSTEM_PROMPT
)

LOG_FILE = "brainbox_logs.csv"

def save_to_csv(username, question, answer):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Username', 'Question', 'Answer'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clean_q = question.replace('\n', ' ').replace(',', ';')
        clean_a = answer.replace('\n', ' ').replace(',', ';')
        writer.writerow([timestamp, username, clean_q, clean_a])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "username" not in st.session_state:
    st.session_state.username = None

st.title("BrainBox NG 🧠🇳🇬")
st.caption("Your Nigerian AI Assistant - Built by Dare Temitayo")

if st.session_state.username is None:
    username = st.text_input("Enter your name to start, boss:", key="name_input")
    if username:
        st.session_state.username = username
        st.rerun()
    else:
        st.stop()

if st.session_state.username.lower() == "dare temitayo":
    with st.sidebar:
        st.header("CEO Dashboard 👑")
        st.success(f"Welcome back, Oga {st.session_state.username}")
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            st.metric("Total Chats Logged", len(df))
            with open(LOG_FILE, 'rb') as f:
                st.download_button(
                    label="📥 Download All Logs",
                    data=f,
                    file_name="brainbox_logs.csv",
                    mime="text/csv"
                )
        else:
            st.info("No logs yet. Make users chat first.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(f"Wetin you wan know, {st.session_state.username}?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.chat_message("assistant"):
            with st.spinner("BrainBox dey think..."):
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                answer = response.text
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_to_csv(st.session_state.username, prompt, answer)
    except Exception as e:
        st.error(f"BrainBox hang small: {str(e)}")
        st.info("Check your GEMINI_API_KEY for Streamlit Secrets or try again.")
