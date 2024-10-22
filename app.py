import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def call_xai_api(user_input):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a test assistant."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

st.title("X.AI Chat Completion Demo")

user_input = st.text_input("Enter your message:", "Testing. Just say hi and hello world and nothing else.")

if st.button("Send"):
    if os.getenv('XAI_API_KEY'):
        with st.spinner("Calling X.AI API..."):
            response = call_xai_api(user_input)
        
        st.subheader("API Response:")
        st.json(response)
        
        if "choices" in response and len(response["choices"]) > 0:
            message_content = response["choices"][0]["message"]["content"]
            st.subheader("Assistant's Response:")
            st.write(message_content)
        else:
            st.error("No response content found in the API response.")
    else:
        st.error("API key not found. Please set the XAI_API_KEY in your .env file.")

st.sidebar.info("This app now uses a .env file to store the API key securely.")
