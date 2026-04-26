import streamlit as st
from gradio_client import Client
import os

# Page Configuration
st.set_page_config(page_title="Alpha AI 3D World Gen", page_icon="🌌")

st.title("🌌 Alpha AI: HY-World 2.0 Tester")
st.subheader("Generate 3D Worlds using ZeroGPU Tech")

# Space URL (ඔබ දුන්න ලින්ක් එක)
SPACE_URL = "https://prithivmlmods-hy-world-2-0-demo.hf.space"

# Sidebar for settings
st.sidebar.header("Settings")
status_placeholder = st.sidebar.empty()

# Prompt Input
user_prompt = st.text_input("Enter your World Description:", placeholder="A futuristic Cybertron city with glowing lights...")

if st.button("Generate 3D World"):
    if user_prompt:
        try:
            status_placeholder.warning("⏳ ZeroGPU සක්‍රිය වෙමින් පවතී... (විනාඩියක් පමණ යයි)")
            
            # Gradio Client සම්බන්ධ කිරීම
            client = Client(SPACE_URL)
            
            # API එකට පණිවිඩය යැවීම
            # සටහන: බොහෝ ZeroGPU Space වල ප්‍රධාන API එක /predict වේ
            result = client.predict(
                prompt=user_prompt,
                api_name="/predict"
            )
            
            if result:
                status_placeholder.success("✅ සාර්ථකව නිම කළා!")
                st.write("### Generated Result:")
                
                # ලැබෙන ප්‍රතිඵලය පෙන්වීම (වීඩියෝ එකක් හෝ පින්තූරයක් නම්)
                if isinstance(result, str) and (result.endswith('.mp4') or result.endswith('.webm')):
                    st.video(result)
                elif isinstance(result, str) and (result.endswith('.jpg') or result.endswith('.png')):
                    st.image(result)
                else:
                    st.write(f"Download Result: [Click Here]({result})")
                    st.info("සටහන: මෙය Gaussian Splatting (.ply) ගොනුවක් නම්, එය බ්ලෙන්ඩර් එකේදී විවෘත කරන්න.")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
            status_placeholder.error("❌ Connection Failed")
    else:
        st.warning("කරුණාකර ප්‍රොම්ප්ට් එකක් ඇතුළත් කරන්න.")

st.markdown("---")
st.caption("Powered by Alpha AI & ZeroGPU Technology")
