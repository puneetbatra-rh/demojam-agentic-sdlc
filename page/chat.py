# for communication with Llama Stack
from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client import RAGDocument
from llama_stack_client.lib.agents.react.agent import ReActAgent
from llama_stack_client.lib.agents.react.tool_parser import ReActOutput

# pretty print of the results returned from the model/agent
from termcolor import cprint
import sys
sys.path.append('..')  
import uuid
import os

from dotenv import load_dotenv
load_dotenv()
import streamlit as st

tavily_search_api_key = os.getenv("TAVILY_SEARCH_API_KEY")
base_url = os.getenv("REMOTE_BASE_URL")
provider_data = {"tavily_search_api_key": tavily_search_api_key}
client = LlamaStackClient(
    base_url=base_url,
    provider_data=provider_data
)




# Sidebar configurations
with st.sidebar:
    st.header("Configuration")
    available_models = client.models.list()
    available_models = [model.identifier for model in available_models if model.model_type == "llm"]
    selected_model = st.selectbox(
        "Choose a model",
        available_models,
        index=0,
    )

    temperature = float(os.getenv("TEMPERATURE"))

    top_p = float(os.getenv("TEMPERATURE"))

    max_tokens = float(os.getenv("MAX_TOKENS"))

    stream = os.getenv("STREAM")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant.",
        help="Initial instructions given to the AI to set its behavior and context",
    )

    # Add clear chat button to sidebar
    if st.button("Start a new request", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Main chat interface
logo_path = "images/logo.png" 
st.image(logo_path, width=200)
st.title("DemoJam Red Hat One 2026")
st.markdown("""## Agentic AI System for Software Development Lifycle Automation""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.text_area("Example: Can you help me build a chatbot for bank that can take input from the customer?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if temperature > 0.0:
            strategy = {
                "type": "top_p",
                "temperature": temperature,
                "top_p": top_p,
            }
        else:
            strategy = {"type": "greedy"}

        response = client.inference.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            model_id=selected_model,
            stream=stream,
            sampling_params={
                "strategy": strategy,
                "max_tokens": max_tokens,
            },
        )

        if stream:
            for chunk in response:
                if chunk.event.event_type == "progress":
                    full_response += chunk.event.delta.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        else:
            full_response = response.completion_message.content
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

