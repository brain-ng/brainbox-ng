import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BrainBox NG", page_icon="🤖")

st.title("BrainBox NG 🤖")
st.caption("Your Nigerian AI Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = model.generate_content(prompt).text
        st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
