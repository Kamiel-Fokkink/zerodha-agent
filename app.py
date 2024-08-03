
import streamlit as st
import ai


st.set_page_config(
    page_title="Zerodha knowledge agent",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Zerodha knowledge agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about Zerodha"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = ai.ask(st.session_state.messages)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})