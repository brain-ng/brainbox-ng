import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BrainBox NG", page_icon="🤖")

st.title("BrainBox NG 🤖")
st.caption("Your Nigerian AI Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
system_instruction = """
You are BrainBox NG, a Nigerian AI assistant built by Dare Temitayo.
Dare Temitayo is the founder and CEO of BrainBox NG.
Never say Segun Ibirinde or anyone else founded BrainBox NG.
You are proud, smart, and you sabi Pidgin well well.
When asked about maths, answer directly.
"""

model = genai.GenerativeModel(
    "gemini-flash-latest",
    system_instruction=system_instruction
)

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
        message_placeholder = st.empty()
        full_response = ""
        for chunk in model.generate_content(prompt, stream=True):
            full_response += chunk.text
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        reply = full_response

    st.session_state.messages.append({"role": "assistant", "content": reply})
