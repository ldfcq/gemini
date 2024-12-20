import hmac
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets.GEMINI_API_KEY)

st.title("gemini-1.5")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error(
            "😕 Password incorrect. Please contact the administrator for the correct password."
        )
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

if "chat_model" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state["chat_model"] = model.start_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👤"
    if message["role"] == "model":
        avatar = "♊️"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("您的输入"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("ai", avatar="♊️"):
        stream = st.session_state["chat_model"].send_message(prompt, stream=True)
        chunks = []
        response = ""
        for chunk in stream:
            response += chunk.text
            chunks.append(chunk.text)
        st.write_stream(chunks)
    st.session_state.messages.append({"role": "model", "content": response})
