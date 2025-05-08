from dotenv import load_dotenv
import streamlit as st
import os

def init_keys():
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key is None:
        print("OPENAI_API_KEY is not set in the .env file.")
        openai_api_key = st.secrets["api_keys"]["openai"]

        if openai_api_key is None:
            raise ValueError("OPENAI_API_KEY is not set in the secrets.")
        else:
            print("OPENAI_API_KEY is set in the streamlit secrets.")
    else:
        print("OPENAI_API_KEY is set in the .env file.")

    return openai_api_key
