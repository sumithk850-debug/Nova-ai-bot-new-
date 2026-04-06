import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# 1. AI Configuration (ඔබේ API Key එක මෙතැනට දෙන්න)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Alpha AI 3D", layout="wide")
st.title("🚀 Alpha AI - Mobile 3D Engine")

# පද්ධතියේ ක්‍රියාකාරීත්වය පැහැදිලි කරන රූපසටහනක්
# 

# 2. User Input
user_prompt = st.chat_input("මොන වගේ 3D නිර්මාණයක්ද ඕනේ? (උදා: රතු පාට කැරකෙන පිරමීඩයක් හදන්න)")

if user_prompt:
    with st.spinner("ඇල්ෆා AI නිර්මාණය කරමින් පවතිී..."):
        # 3. AI එකෙන් Three.js Code එක ලබා ගැනීම
        system_instruction = "Respond ONLY with a complete HTML/Three.js code. No text, no markdown. Use OrbitControls. Make it mobile-friendly."
        response = model.generate_content(f"{system_instruction} \n\n User request: {user_prompt}")
        
        # අනවශ්‍ය ```html වැනි කොටස් ඉවත් කිරීම
        clean_code = response.text.replace("```html", "").replace("```", "").strip()

        # 4. 3D Viewer එක පෙන්වීම
        st.subheader("සජීවී 3D දර්ශනය")
        components.html(clean_code, height=500, scrolling=True)

        # 5. Code එක බලා ගැනීමට අවශ්‍ය නම් (Optional)
        with st.expander("Source Code එක බලන්න"):
            st.code(clean_code, language="html")

else:
    st.info("පහළ ඇති box එකේ යමක් ටයිප් කර ඇල්ෆා AI එකට විධානයක් දෙන්න.")
