import streamlit as st
from gradio_client import Client
import os

st.set_page_config(page_title="Alpha AI 3D World Gen", page_icon="🌌")
st.title("🌌 Alpha AI: HY-World 2.0 Tester")

SPACE_URL = "https://prithivmlmods-hy-world-2-0-demo.hf.space"

user_prompt = st.text_input("Enter your World Description:")

if st.button("Generate 3D World"):
    if user_prompt:
        try:
            st.info("⏳ ZeroGPU සක්‍රියයි... (විනාඩියක් පමණ ඉවසන්න)")
            client = Client(SPACE_URL)
            
            # මෙන්න මෙතන මම වෙනසක් කළා: api_name="/predict" වෙනුවට 
            # කෙලින්ම index එක පාවිච්චි කරනවා.
            # HY-World 2.0 සඳහා බොහෝ විට මෙය පරාමිතීන් කිහිපයක් ගනී.
            # [prompt, seed, randomize_seed, width, height, guidance_scale, num_inference_steps]
            
            result = client.predict(
                user_prompt,	# Prompt
                0,              # Seed
                True,           # Randomize Seed
                1024,           # Width
                1024,           # Height
                6,              # Guidance Scale
                20,             # Steps
                api_name="/infer" # HY-World 2.0 හි නම බොහෝ විට /infer වේ
            )
            
            if result:
                st.success("✅ වැඩේ හරි!")
                # HY-World 2.0 වීඩියෝවක් ලබා දෙන්නේ නම්:
                if isinstance(result, tuple):
                    st.video(result[0])
                else:
                    st.write(f"Result: {result}")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("කරුණාකර ප්‍රොම්ප්ට් එකක් ඇතුළත් කරන්න.")
