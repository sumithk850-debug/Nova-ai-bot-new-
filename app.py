import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Secure API Key Loading
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# Set up Model
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Nova AI")
st.caption("Developed by: Hasith")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Nova..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check if your API Key is active at Google AI Studio.")
