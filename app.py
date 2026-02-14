import streamlit as st
import google.generativeai as genai

# Setup Page
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Fetch API Key from Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("Missing GEMINI_API_KEY in Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Config Error: {e}")
    st.stop()

# Initialize Gemini Pro Model
model = genai.GenerativeModel('gemini-pro')

st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Message Nova..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate response
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Nova encountered an error: {e}")
