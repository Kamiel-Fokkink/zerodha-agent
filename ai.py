from openai import OpenAI
import chromadb
import os
import streamlit as st

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

os.environ["TOKENIZERS_PARALLELISM"] = "false"
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def rag(question):
    chroma_client = chromadb.PersistentClient("database/")
    collection = chroma_client.get_or_create_collection(name="zerodhadb")
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    return results['documents'][0]


def ask(messages):
    if len(messages) == 1:
        context = rag(messages[0]["content"])
        instruction = f"""You are a knowledgeable assistant specialized in providing accurate and concise answers based on the provided knowledge base. Use the following information to respond to user queries:
## Page 1: 
{context[0]}
## Page 2: 
{context[1]}
## Page 3: 
{context[2]}
Answer the questions clearly and directly based on the provided information. If the answer is not available in the knowledge base, indicate that the information is not available."""
        messages.insert(0, {"role": "system", "content": instruction})
        st.session_state.messages = messages
    stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ],
            stream=True,
        )
    return stream