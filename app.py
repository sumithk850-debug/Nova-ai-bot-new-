import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# API Key Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# Using the best stable model: gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling
if prompt := st.chat_input("Ask Nova anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate response from Gemini 1.5 Flash
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure your API Key is correct and Reboot the app.")
