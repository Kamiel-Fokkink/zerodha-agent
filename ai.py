__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from openai import OpenAI
import chromadb
import os
import streamlit as st
import requests
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
assistant1 = "asst_HajGJEEyPDGCefVu32KV6f3I"
assistant2 = "asst_NWmIKGZK3eyzyNxsY2uDJaU3"


def rag(question):
    chroma_client = chromadb.PersistentClient("database/")
    collection = chroma_client.get_or_create_collection(name="zerodhadb")
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    doc_string = [f"Document {i+1}\n{doc}" for i, doc in enumerate(results['documents'][0])]
    return '\n\n'.join(doc_string)


def check_run(thread_id, run_id):
    endpoint = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}"
    try:
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}", "OpenAI-Beta": "assistants=v2"}, timeout=5)
        response.raise_for_status()
        return response.json()["completed_at"] is not None
    except requests.exceptions.RequestException:
        return False
    

def run_thread(thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    done = False
    while not done:
        time.sleep(2)
        done = check_run(thread_id, run.id)

    return client.beta.threads.messages.list(thread_id).data[0].content[0].text.value


def agent1(messages):
    if "agent1_thread" not in st.session_state:
        st.session_state["agent1_thread"] = client.beta.threads.create(messages=messages)
    else:
        client.beta.threads.messages.create(
            thread_id=st.session_state["agent1_thread"].id,
            role="user",
            content=messages[-1]["content"]
        )
    keywords = run_thread(st.session_state["agent1_thread"].id, assistant1)
    documents = rag(keywords)
    client.beta.threads.messages.create(
        thread_id=st.session_state["agent1_thread"].id,
        role="user",
        content=documents
    )
    return run_thread(st.session_state["agent1_thread"].id, assistant1)


def agent2(messages):
    messages.append({"role": "user", "content": agent1(messages)})
    if "agent2_thread" not in st.session_state:
        st.session_state["agent2_thread"] = client.beta.threads.create(messages=messages)
    else:
        client.beta.threads.messages.create(
            thread_id=st.session_state["agent2_thread"].id,
            role="user",
            content=messages[-1]["content"]
        )
    return run_thread(st.session_state["agent2_thread"].id, assistant2)