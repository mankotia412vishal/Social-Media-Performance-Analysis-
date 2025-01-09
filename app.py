import pathlib
import streamlit as st
import requests
import json
from typing import Optional
from dotenv import load_dotenv
import os
from frontent import show_graph

# Load environment variables
load_dotenv()

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.getenv('LANGFLOW_ID')
FLOW_ID = os.getenv('FLOW_ID')
APPLICATION_TOKEN = os.getenv('APPLICATION_TOKEN')
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# Tweaks Dictionary
TWEAKS = {
    "ChatInput-DWQpc": {},
    "Prompt-XxSEq": {},
    "ChatOutput-mlcoa": {},
    "GoogleGenerativeAIModel-DX1hx": {}
}

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style> {f.read()} </style> ")

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

# Add custom CSS for styling the chat input container
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Change background color of chat input container */
        .stChatInputContainer > div {
            background-color: #fff;
            border: 1px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to interact with Langflow API
def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }

    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)
    return response

# Streamlit Main Application
def main():
    st.title("Social Media Engagement Analysis")
    # Add custom CSS for centered spinner
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }
        .spinner-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .spinner {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .stTextInput input[aria-label="test color"] {
            background-color: #0066cc;
            color: #33ff33;
        }
        .custom-container {
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        div[data-testid="stChatInput"]{
            border: 1px solid yellow;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Custom CSS for font styling
    st.markdown(
        """
        <style>
        .title {
            font-family: 'Times New Roman', sans-serif;  /* Change to your preferred font */
            font-size: 36px;
            color: #4CAF50;  /* Optional: change text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("History")
    st.sidebar.markdown("See your previous chats here.")
    # Add more sidebar elements as needed
    st.sidebar.selectbox("Select an option", ["Posts", "Reels", "Carousels"])
    # st.markdown('<h2 class="title">Your Custom Title</h2>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Custom container for chat input with shadow
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    prompt = st.chat_input("Say Something...")
    st.markdown('</div>', unsafe_allow_html=True)
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        spinner_placeholder = st.empty()
        spinner_placeholder.markdown('<div class="spinner-overlay"><div class="spinner"></div></div>', unsafe_allow_html=True)
        response = run_flow(
            message=prompt,
            endpoint=ENDPOINT or FLOW_ID,
            output_type="chat",
            input_type="chat",
            tweaks=TWEAKS,
            application_token=APPLICATION_TOKEN
        )
        spinner_placeholder.empty()
        try:
            response_content = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "Error: No response from the API")
            response_content = response_content.replace("`", "").replace("json", "").replace("\n", "").replace("Gemni can make mistakes. Check important info.", "")
            response_content = json.loads(response_content)
        except (json.JSONDecodeError, AttributeError):
            response_content = {"response_to_query": "Google Generative AI: Gemni LLM Resource has been exhausted (e.g. check quota)..", "Graph": "No"}

        st.session_state.messages.append({"role": "assistant", "content": response_content.get('response_to_query', 'Error: Missing response')})
        st.session_state.messages.append({"Graph": response_content.get('Graph', 'No')})

    # Display chat messages and graphs
    for message in st.session_state.messages:
        if isinstance(message, dict) and "Graph" in message:
            if message["Graph"] == "Yes":
                show_graph()  # Show graph immediately after related content
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

if __name__ == "__main__":
    main()
