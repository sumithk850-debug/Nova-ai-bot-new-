import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="Alpha AI - HY-World", page_icon="🌌")
st.title("🌌 Alpha AI: HY-World 2.0 Tester")

# API URL
SPACE_URL = "https://prithivmlmods-hy-world-2-0-demo.hf.space"

user_prompt = st.text_input("Enter your World Description:", value="A cybertronian base")

if st.button("Generate"):
    if user_prompt:
        try:
            st.info("⏳ ZeroGPU සක්‍රිය වෙමින් පවතී... විනාඩියක් පමණ රැඳී සිටින්න.")
            client = Client(SPACE_URL)
            
            # HY-World 2.0 හි පරාමිතීන් ටික ලැයිස්තුවක් ලෙස යැවිය යුතුය.
            # පයිතන් වල මෙය [ ] වරහන් ඇතුළත දැමිය යුතුයි.
            
            result = client.predict(
                [user_prompt],  # ප්‍රොම්ප්ට් එක ලිස්ට් එකක් ලෙස (List of Strings)
                0,              # Seed
                True,           # Randomize seed
                1024,           # Width
                1024,           # Height
                6,              # Guidance scale
                20,             # Number of inference steps
                fn_index=0      
            )
            
            if result:
                st.success("✅ සාර්ථකයි!")
                # HY-World සාමාන්‍යයෙන් වීඩියෝවක path එකක් හෝ gallery එකක් ලබා දෙයි.
                if isinstance(result, (list, tuple)):
                    st.video(result[0])
                else:
                    st.video(result)
                    
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
    else:
        st.warning("ප්‍රොම්ප්ට් එකක් ඇතුළත් කරන්න.")
