import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Fetch API Key from Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Config Error: {e}")
    st.stop()

# Using the latest Gemini 2.0 Flash model
model = genai.GenerativeModel('gemini-2.0-flash')

st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
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
            # Getting response from Gemini 2.0 Flash
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check your API Key or Reboot the app.")
