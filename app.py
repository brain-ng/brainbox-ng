import streamlit as st
import openai
import os

st.set_page_config(page_title="BrainBox NG", page_icon="🇳🇬")

st.title("🇳🇬 BrainBox NG")
st.subheader("Your Nigerian AI for WAEC & JAMB")

# Get API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# System prompt to make it Nigerian
system_prompt = """
You are BrainBox NG, a friendly Nigerian AI tutor.
You help students with WAEC, JAMB, NECO questions.
Explain in simple English. Use Nigerian examples like Jollof, NEPA, Danfo.
Be encouraging. Call user 'Boss' or 'Chief' sometimes.
Keep answers short and clear for mobile users.
"""

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Show old messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask BrainBox NG anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("BrainBox NG dey think..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})import streamlit as st
import openai
import os

st.set_page_config(page_title="BrainBox NG", page_icon="🇳🇬")

st.title("🇳🇬 BrainBox NG")
st.subheader("Your Nigerian AI for WAEC & JAMB")

# Get API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# System prompt to make it Nigerian
system_prompt = """
You are BrainBox NG, a friendly Nigerian AI tutor.
You help students with WAEC, JAMB, NECO questions.
Explain in simple English. Use Nigerian examples like Jollof, NEPA, Danfo.
Be encouraging. Call user 'Boss' or 'Chief' sometimes.
Keep answers short and clear for mobile users.
"""

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Show old messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask BrainBox NG anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("BrainBox NG dey think..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
