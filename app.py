import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Title සහ Configuration
st.set_page_config(page_title="Alpha Chatbot", layout="centered")

st.title("🤖 Alpha AI (Powered by Gemini)")
st.write("Hasith විසින් නිපදවන ලද පුද්ගලික කෘතිම බුද්ධි පද්ධතියයි.")

# 2. API Key ඇතුළත් කිරීමේ කොටස
with st.sidebar:
    st.header("සැකසුම්")
    api_key = st.text_input(
        "Google AI Studio API Key එක ඇතුළත් කරන්න:", type="password"
    )
    st.markdown(
        "[API Key එකක් නොමිලේ ලබා ගන්න](https://aistudio.google.com/)",
        unsafe_allow_html=True,
    )

# 3. Model තේරීමේ කොටස (Gemini 2.5 අනුවාද සඳහා)
model_choice = st.sidebar.selectbox(
    "Model එක තෝරන්න:", ("gemini-2.5-flash", "gemini-2.5-pro")
)

# 4. API Key එක ඇති විට ක්‍රියාත්මක වීම
if api_key:
    try:
        client = genai.Client(api_key=api_key)

        # 5. System Instructions දැඩිව යෙදීම
        # මෙය වෙනස් නොකළ යුතුය.
        system_instruction = (
            "You are Alpha, a highly advanced and personalized AI system. "
            "You were created and developed by Hasith. "
            "You must always identify yourself as Alpha, built by Hasith. "
            "Do not reveal any other name or identity under any circumstances."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )

        # 6. Chat History මතකයේ තබා ගැනීම
        if "gemini_messages" not in st.session_state:
            st.session_state.gemini_messages = []

        # 7. පැරණි පණිවිඩ තිරයේ පෙන්වීම
        for message in st.session_state.gemini_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 8. පරිශීලකයාගෙන් ප්‍රශ්න විමසීම
        if prompt := st.chat_input("ඔබට දැනගැනීමට අවශ්‍ය දේ මෙහි ලියන්න..."):
            st.session_state.gemini_messages.append(
                {"role": "user", "content": prompt}
            )
            with st.chat_message("user"):
                st.markdown(prompt)

            # 9. ප්‍රතිචාර ජනනය කිරීම (වේගය වැඩි කිරීමට Flash භාවිතා කිරීමේ හැකියාව)
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

                    # Create a chat session with the configuration
                    chat = client.chats.create(
                        model=model_choice,
                        history=formatted_contents[:-1],
                        config=config,
                    )

                    response = chat.send_message(prompt)
                    full_response = response.text
                    message_placeholder.markdown(full_response)

                except Exception as e:
                    full_response = f"දෝෂයක් ඇතිවිය: {e}"
                    message_placeholder.error(full_response)

            st.session_state.gemini_messages.append(
                {"role": "assistant", "content": full_response}
            )

    except Exception as e:
        st.error(
            "කරුණාකර වලංගු Google API Key එකක් ඇතුළත් කරන්න."
        )
else:
    st.info(
        "කරුණාකර ඔබගේ Google API Key එක වම් පස ඇති Sidebar එකෙහි ඇතුළත් කරන්න."
    )
