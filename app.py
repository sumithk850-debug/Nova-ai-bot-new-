import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="Alpha AI - HY-World", page_icon="🌌")
st.title("🌌 Alpha AI: HY-World 2.0 Tester")

SPACE_URL = "https://prithivmlmods-hy-world-2-0-demo.hf.space"

user_prompt = st.text_input("Enter your World Description:", value="A cybertronian base")

if st.button("Generate"):
    if user_prompt:
        try:
            st.info("⏳ ZeroGPU සක්‍රිය වෙමින් පවතී... විනාඩියක් පමණ රැඳී සිටින්න.")
            client = Client(SPACE_URL)
            
            # මෙතනදී අපි api_name පාවිච්චි කරන්නේ නැහැ. 
            # ඒ වෙනුවට පළමු function එකට (0) අදාළ parameters ටික දෙනවා.
            # HY-World 2.0 සඳහා අවශ්‍ය පරාමිතීන් පිළිවෙලින්:
            result = client.predict(
                user_prompt,    # Prompt (String)
                0,              # Seed (Number)
                True,           # Randomize seed (Boolean)
                1024,           # Width
                1024,           # Height
                6,              # Guidance scale
                20,             # Number of inference steps
                fn_index=0      # <--- මෙන්න මේකයි වැදගත්! API නම වෙනුවට අංකය දෙනවා.
            )
            
            if result:
                st.success("✅ සාර්ථකයි!")
                # HY-World සාමාන්‍යයෙන් වීඩියෝවක් ලබා දෙයි. 
                # result එකේ පළමු අගය (index 0) වීඩියෝ ලින්ක් එකයි.
                if isinstance(result, (list, tuple)):
                    st.video(result[0])
                else:
                    st.video(result)
                    
        except Exception as e:
            st.error(f"❌ API එකට සම්බන්ධ විය නොහැක: {str(e)}")
    else:
        st.warning("ප්‍රොම්ප්ට් එකක් ඇතුළත් කරන්න.")
