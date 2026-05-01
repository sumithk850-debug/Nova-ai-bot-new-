import os
import streamlit as st
from openai import OpenAI

# 1. Page Title සහ Configuration
st.set_page_config(page_title="Cerebras GPT-OSS 120B Chatbot", layout="centered")

st.title("🤖 Cerebras GPT-OSS 120B Chatbot")
st.write("Cerebras Inference API භාවිතයෙන් ක්‍රියාත්මක වන ප්‍රබල AI ආකෘතියකි.")

# 2. API Key ඇතුළත් කිරීමේ කොටස (Sidebar එකේ)
with st.sidebar:
    st.header("සැකසුම්")
    api_key = st.text_input(
        "Cerebras API Key එක ඇතුළත් කරන්න:", type="password"
    )
    st.markdown(
        "[API Key එකක් නොමිලේ ලබා ගන්න](https://inference.cerebras.ai/)",
        unsafe_allow_html=True,
    )

# 3. OpenAI Client එක සකස් කිරීම
if api_key:
    try:
        client = OpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=api_key,
        )

        # 4. Chat History (ඉතිහාසය) මතකයේ තබා ගැනීම
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 5. පැරණි පණිවිඩ තිරයේ පෙන්වීම
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 6. පරිශීලකයාගෙන් ප්‍රශ්න විමසීම
        if prompt := st.chat_input("ඔබට දැනගැනීමට අවශ්‍ය දේ මෙහි ලියන්න..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 7. ප්‍රතිචාර ජනනය කිරීම
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                try:
                    completion = client.chat.completions.create(
                        model="gpt-oss-120b",  # Model එක මෙහි සඳහන් වේ
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        temperature=0.7,
                    )

                    full_response = completion.choices[
                        0
                    ].message.content
                    message_placeholder.markdown(full_response)

                except Exception as e:
                    full_response = f"දෝෂයක් ඇතිවිය: {e}"
                    message_placeholder.error(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

    except Exception as e:
        st.error(
            "කරුණාකර නිවැරදි Cerebras API Key එකක් ඇතුළත් කරන්න."
        )
else:
    st.info(
        "කරුණාකර ඔබගේ Cerebras API Key එක වම් පස ඇති Sidebar එකෙහි ඇතුළත් කරන්න."
    )
