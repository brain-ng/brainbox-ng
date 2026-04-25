import streamlit as st
from google import genai  # NEW IMPORT
from google.genai import types  # NEW IMPORT
import os
import pandas as pd
from datetime import datetime
import csv

st.set_page_config(
    page_title="BrainBox NG 🇳🇬", 
    page_icon="🧠",
    layout="centered"
)

# NEW CLIENT SETUP 👇
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
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
    try:  # 4 spaces indent
        with st.chat_message("assistant"):  # 8 spaces
            with st.spinner("BrainBox dey think..."):  # 12 spaces
                response = client.models.generate_content(  # 16 spaces
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )
                answer = response.text  # 16 spaces
                st.markdown(answer)  # 16 spaces
        st.session_state.messages.append({"role": "assistant", "content": answer})  # 8 spaces
        save_to_csv(st.session_state.username, prompt, answer)  # 8 spaces
    except Exception as e:  # 4 spaces - SAME AS 'try'
        if "RESOURCE_EXHAUSTED" in str(e):  # 8 spaces
            st.warning("BrainBox dey rest small abeg 😅 Too many people dey chat right now")  # 12 spaces
            st.info("Wait 1 minute then ask again, boss.")  # 12 spaces
            st.stop()  # 12 spaces
        else:  # 8 spaces
            st.error(f"BrainBox hang small: {str(e)}")  # 12 spaces
