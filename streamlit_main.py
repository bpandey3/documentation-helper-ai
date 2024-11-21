from typing import Set

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

# Page config for a cleaner look
st.set_page_config(
    page_title="RAG based Documentation search",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stSpinner > div {
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main header with better styling
st.markdown("""
    <h1 style='text-align: center; margin-bottom: 30px;'>
        Documentation Search Assistant 🔍
    </h1>
    """, unsafe_allow_html=True)

# Initialize session state
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

# Chat container with custom styling
chat_container = st.container()
with chat_container:
    # Display chat history
    if st.session_state.get("chat_answers_history"):
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            message(user_query, is_user=True, key=f"user_{len(st.session_state['chat_answers_history'])}")
            message(generated_response, key=f"assistant_{len(st.session_state['chat_answers_history'])}")

# Input area with better styling
st.markdown("<div style='padding: 30px'></div>", unsafe_allow_html=True)
input_container = st.container()
with input_container:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        prompt = st.text_input(
            "",
            placeholder="Ask me anything about the documentation...",
            key="user_input",
        )

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "\n\n**Sources:**\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

# Handle user input
if prompt:
    with st.spinner("🤔 Thinking..."):
        generated_response = run_llm(query=prompt)
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        
        # Rerun to update the chat immediately
        #st.experimental_rerun()