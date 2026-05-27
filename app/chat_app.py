
import select
import traceback
import os 
import streamlit as st 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def initialize():
    st.set_page_config(
        page_title = "My Chat App",
    )
    st.header("チャットアプリ")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []


def select_model(temparature=0): 
    models = ("Gemini-2.5-flash", "GPT-OSS-120B")
    model = st.sidebar.radio("Choose a model", models)
    
    if model == "Gemini-2.5-flash":
        llm = ChatGoogleGenerativeAI(model = model, api_key = GEMINI_API_KEY)
    elif model == "GPT-OSS-120B":
        llm = ChatOpenAI(
        model = "openai/gpt-oss-120b:free",
        api_key = OPENROUTER_API_KEY,
        base_url = "https://openrouter.ai/api/v1"
        )

def chat_with_history():

    #display  chat messages。最初は何も入ってないから実行されない
    for message in st.session_state["messages"]:
        with st.chat_input

    if prompt := st.chat_input("Say something"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state["messages"].append({"role": "user", "content": prompt})


    for message in st.session_state["messages"]:
        with st.chat_message()

output_parser = StrOutputParser()
chain = prompt | llm | output_parser
chain2 = prompt | llm | output_parser
response = chain.invoke({"input": "こんにちは, 君の名前は？"})
response2 = chain2.invoke({"input": "こんにちは、てめーの名前は？"})

print(response)
print("------")
print(response2)