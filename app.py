import os
import streamlit as st
from google import genai

# 1. Page Title සහ Configuration
st.set_page_config(page_title="Gemini 1.5 Chatbot", layout="centered")

st.title("🤖 Gemini 1.5 Pro/Flash Chatbot")
st.write("Google AI Studio හි නිල Gemini API භාවිතයෙන් ක්‍රියාත්මක වේ.")

# 2. API Key ඇතුළත් කිරීමේ කොටස (Sidebar එකේ)
with st.sidebar:
    st.header("සැකසුම්")
    api_key = st.text_input(
        "Google AI Studio API Key එක ඇතුළත් කරන්න:", type="password"
    )
    st.markdown(
        "[API Key එකක් නොමිලේ ලබා ගන්න](https://aistudio.google.com/)",
        unsafe_allow_html=True,
    )

# 3. Model තේරීමේ කොටස (Sidebar එකේ)
model_choice = st.sidebar.selectbox(
    "Model එක තෝරන්න:", ("gemini-1.5-flash", "gemini-1.5-pro")
)

# 4. API Key එක ඇති විට ක්‍රියාත්මක වීම
if api_key:
    try:
        # නවතම google-genai client එක සකස් කිරීම
        client = genai.Client(api_key=api_key)

        # 5. Chat History මතකයේ තබා ගැනීම
        if "gemini_messages" not in st.session_state:
            st.session_state.gemini_messages = []

        # 6. පැරණි පණිවිඩ තිරයේ පෙන්වීම
        for message in st.session_state.gemini_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 7. පරිශීලකයාගෙන් ප්‍රශ්න විමසීම
        if prompt := st.chat_input("ඔබට දැනගැනීමට අවශ්‍ය දේ මෙහි ලියන්න..."):
            # පරිශීලකයාගේ පණිවිඩය එකතු කිරීම
            st.session_state.gemini_messages.append(
                {"role": "user", "content": prompt}
            )
            with st.chat_message("user"):
                st.markdown(prompt)

            # 8. ප්‍රතිචාර ජනනය කිරීම
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                try:
                    # සංවාදයේ පැරණි පණිවිඩ API එකට යැවීමට ගැලපීම
                    formatted_contents = []
                    for m in st.session_state.gemini_messages:
                        # gemini api එකට user/model ලෙස role අවශ්‍ය වේ
                        role = (
                            "user" if m["role"] == "user" else "model"
                        )
                        formatted_contents.append(
                            {
                                "role": role,
                                "parts": [{"text": m["content"]}],
                            }
                        )

                    # API ඉල්ලීම යැවීම
                    response = client.chats.create(
                        model=model_choice,
                        history=formatted_contents[:-1],  # ඉතිහාසය
                    )

                    # නවතම පණිවිඩයට පිළිතුර ලබා ගැනීම
                    result = response.send_message(prompt)
                    full_response = result.text
                    message_placeholder.markdown(full_response)

                except Exception as e:
                    full_response = f"දෝෂයක් ඇතිවිය: {e}"
                    message_placeholder.error(full_response)

            # සහායකයාගේ පණිවිඩය එකතු කිරීම
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
