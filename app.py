import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Groq Configuration
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Alpha AI 3D Engine", layout="wide")
st.title("🏎️ Alpha AI - Real 3D Object Generator")

# 2. User Input
user_prompt = st.chat_input("මොකක්ද ඕනේ? (උදා: A realistic sports car)")

if user_prompt:
    with st.spinner("ඇල්ෆා AI රූපය නිර්මාණය කරමින් පවතී..."):
        # 3. System Prompt එක වෙනස් කිරීම
        # මෙහිදී අපි AI එකට කියනවා Sketchfab හෝ පොදු 3D repository එකකින් Model එකක් ගන්න කියලා
        system_msg = """
        You are a 3D Web Engine. If the user asks for an object like a 'Car', 'Truck', or 'Robot', 
        write a complete HTML file using <model-viewer> tag from Google. 
        Use a high-quality glb/gltf source from a public directory or 
        generate a detailed Three.js scene with primitive shapes if a model isn't available.
        Make it interactive (auto-rotate, camera-controls, touch-enabled).
        Respond ONLY with the HTML code. No markdown.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        
        clean_code = chat_completion.choices[0].message.content.replace("```html", "").replace("```", "").strip()

        # 4. Displaying the 3D Viewer
        components.html(clean_code, height=600, scrolling=True)

else:
    st.info("දැන් 'Car' කියලා ටයිප් කරලා බලන්න. ඇල්ෆා AI එක ඒක පෝන් එකේ පෙන්වයි.")
