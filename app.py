import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Connection to Gemini API using Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("API Key not found in Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# AI Model Configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Your name is Nova. You were created by Hasith. You are a professional and friendly AI assistant."
)

# User Interface
st.title("🤖 Nova AI")
st.markdown("---")
st.caption("Developed by: Hasith")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Message Nova..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Nova's response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Connection failed. Check your API Key.")
