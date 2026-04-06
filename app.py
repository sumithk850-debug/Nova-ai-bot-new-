import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. Groq Configuration
# Streamlit Secrets වල 'GROQ_API_KEY' ලෙස ඔබේ Key එක ඇතුළත් කරන්න
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Alpha AI 3D (Groq)", layout="wide")
st.title("🚀 Alpha AI - Powered by Groq 3D")

# 2. User Input
user_prompt = st.chat_input("ඔබට අවශ්‍ය 3D නිර්මාණය ගැන පවසන්න...")

if user_prompt:
    with st.spinner("Groq මඟින් සජීවීව නිර්මාණය කරමින් පවතී..."):
        # 3. Groq හරහා Three.js Code එක ලබා ගැනීම
        system_msg = "You are a 3D expert. Respond ONLY with a complete, single HTML file using Three.js and OrbitControls. Make it mobile-responsive with a dark theme. No explanations, no markdown tags."
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile", # හෝ ඔබ කැමති Groq model එකක්
        )
        
        raw_code = chat_completion.choices[0].message.content
        
        # අනවශ්‍ය markdown (```html) තිබේ නම් ඉවත් කිරීම
        clean_code = raw_code.replace("```html", "").replace("```", "").strip()

        # 4. 3D Viewer එක පෙන්වීම
        st.subheader("සජීවී 3D දර්ශනය (Mobile View)")
        components.html(clean_code, height=500, scrolling=True)

else:
    st.info("පෝන් එකෙන් ඕනෑම 3D විධානයක් ලබා දෙන්න. (උදා: Rotating metallic donut with neon lights)")
