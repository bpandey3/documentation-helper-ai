from typing import Set

from backend.core import run_llm, run_llm2
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
        /* Gradient animated header */
        .title {
            background: linear-gradient(
                to right,
                #12c2e9,
                #c471ed,
                #f64f59
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 5s ease infinite;
            font-size: 4rem !important;
            font-weight: 800 !important;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        
        /* Profile image styling */
        .profile-img {
            border-radius: 50%;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
            display: block;
            margin: 0 auto;
        }
        .profile-img:hover {
            transform: scale(1.05);
        }
        
        /* Input and button styling */
        .stTextInput > div > div > input {
            border-radius: 25px;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #c471ed;
            box-shadow: 0 0 10px rgba(196, 113, 237, 0.3);
        }
        .stButton > button {
            border-radius: 25px;
            padding: 15px 25px;
            font-weight: 600;
            background: linear-gradient(45deg, #12c2e9, #c471ed);
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Results container styling */
        .results-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Custom blockquote style for summary */
        blockquote {
            border-left: 4px solid #c471ed;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
        }
        
        /* Facts list styling */
        .fact-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 10px 15px;
            margin: 8px 0;
            border-left: 4px solid #12c2e9;
        }
        
        /* Fixed input container at bottom */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
            z-index: 100;
        }
        
        /* Add padding at the bottom of chat container to prevent overlap */
        .chat-container {
            margin-bottom: 100px;  /* Space for input container */
            padding-bottom: 20px;
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
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Chat container with custom styling
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
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
st.markdown('</div>', unsafe_allow_html=True)

# Input area with better styling
st.markdown('<div class="input-container">', unsafe_allow_html=True)
input_container = st.container()
with input_container:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        prompt = st.text_input(
            "",
            placeholder="Ask me anything about the documentation...",
            key="user_input",
        )
st.markdown('</div>', unsafe_allow_html=True)

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
            [doc.metadata["source"] for doc in generated_response["context"]]
        )

        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)  
        # Rerun to update the chat immediately
        #st.experimental_rerun()