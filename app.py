
import streamlit as st
import ai


st.set_page_config(
    page_title="Zerodha knowledge agent",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Zerodha knowledge agent")


def conversation(agent, tab):
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about Zerodha", key=tab):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = agent(st.session_state.messages)
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


tab1, tab2 = st.tabs(["1 Agent", "2 Agents"])
with tab1:
    st.session_state.messages = []
    conversation(ai.agent1, 'agent1')
with tab2:
    st.session_state.messages = []
    conversation(ai.agent2, 'agent2')
