import os
import time
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Title සහ Configuration
st.set_page_config(page_title="Alpha Chatbot", layout="centered")

st.title("🤖 Alpha AI (Powered by Gemini)")
st.write("Hasith විසින් නිපදවන ලද පුද්ගලික කෘතිම බුද්ධි පද්ධතියයි.")

# 2. Streamlit Secrets මඟින් API Key එක ලබා ගැනීම
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("කරුණාකර Streamlit Secrets තුළ GEMINI_API_KEY එක සකසන්න.")
    st.stop()

if api_key:
    try:
        client = genai.Client(api_key=api_key)

        # 3. Model තේරීමේ කොටස
        model_choice = st.selectbox(
            "Model එක තෝරන්න:", ("gemini-2.5-flash", "gemini-2.5-pro")
        )

        # 4. System Instructions යාවත්කාලීන කිරීම
        system_instruction = (
            "You are Alpha, a highly advanced and personalized AI system created by Hasith. "
            "Provide direct and helpful answers to the user without repeatedly mentioning who created you."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )

        # 5. Chat History මතකයේ තබා ගැනීම
        if "gemini_messages" not in st.session_state:
            st.session_state.gemini_messages = []

        # 6. පැරණි පණිවිඩ තිරයේ පෙන්වීම
        for message in st.session_state.gemini_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 7. පරිශීලකයාගෙන් ප්‍රශ්න විමසීම
        if prompt := st.chat_input("ඔබට දැනගැනීමට අවශ්‍ය දේ මෙහි ලියන්න..."):
            st.session_state.gemini_messages.append(
                {"role": "user", "content": prompt}
            )
            with st.chat_message("user"):
                st.markdown(prompt)

            # 8. ප්‍රතිචාර ජනනය කිරීම (Spinner සහ Streaming සමඟ)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                try:
                    formatted_contents = []
                    for m in st.session_state.gemini_messages:
                        role = (
                            "user" if m["role"] == "user" else "model"
                        )
                        formatted_contents.append(
                            {
                                "role": role,
                                "parts": [{"text": m["content"]}],
                            }
                        )

                    chat = client.chats.create(
                        model=model_choice,
                        history=formatted_contents[:-1],
                        config=config,
                    )

                    # Spinner එක පෙන්වීම
                    with st.spinner("Alpha සිතමින් සිටී..."):
                        response = chat.send_message(prompt)
                        full_response = response.text

                    # අකුරෙන් අකුර (Streaming) පෙන්වීම
                    streamed_response = ""
                    for chunk in full_response.split():
                        streamed_response += chunk + " "
                        time.sleep(0.02)
                        message_placeholder.markdown(streamed_response + "▌")
                    
                    # අවසාන ප්‍රතිචාරය දෝෂයකින් තොරව සටහන් කිරීම
                    message_placeholder.markdown(full_response)

                except Exception as e:
                    full_response = f"දෝෂයක් ඇතිවිය: {e}"
                    message_placeholder.error(full_response)

            st.session_state.gemini_messages.append(
                {"role": "assistant", "content": full_response}
            )

    except Exception as e:
        st.error(f"දෝෂයක් ඇතිවිය: {e}")
