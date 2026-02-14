import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("API Key missing in Secrets.")
    st.stop()

# Using 'gemini-pro' which is highly stable for v1beta API
model = genai.GenerativeModel('gemini-pro')

st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
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
            st.error(f"Error: {e}")
            st.info("If you see a 404 error again, please wait 5 minutes and Reboot.")
