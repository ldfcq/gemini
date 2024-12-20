import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets.GEMINI_API_KEY)

st.title("gemini-1.5")

if "chat_model" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state["chat_model"] = model.start_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = st.session_state["chat_model"].send_message(prompt, stream=True)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
