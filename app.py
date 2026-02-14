import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Securely fetch API Key from Streamlit Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key_val = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key_val)
    else:
        st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Config Error: {e}")
    st.stop()

# Using the powerful Gemini 1.5 Pro model
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask Nova anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate the response using Gemini 1.5 Pro
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Nova encountered an error: {e}")
            st.info("Try to Reboot the app from the Manage App menu.")
