from typing import Set

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

st.header("RAG based Documentation search")

# Display chat history first
if st.session_state.get("chat_answers_history"):
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)

# Add some spacing before the input
st.write("")
st.write("")

# Move the input to the bottom using columns to center it
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    prompt = st.text_input("Prompt", placeholder="Enter your prompt here..", key="user_input")

# Session state initialization and response generation remain the same
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(query=prompt)
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)