
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


def initialize_app():
    st.set_page_config(
        page_title = "My Chat App",
    )
    st.header("チャットアプリ")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []


def initialize_message():
    if clear_button := st.sidebar.button("Clear Conversation", key="clear"):
        st.session_state["messages"] = [("system", "U R a helpful assistant")]


def select_llm_model(temparature=0): 
    models = ("Gemini-2.5-flash", "GPT-OSS-120B")
    model = st.sidebar.radio("Choose a model", models)
    
    if model == "Gemini-2.5-flash":
        return ChatGoogleGenerativeAI(model = "gemini-2.5-flash", api_key = GEMINI_API_KEY, streaming=True)
        
    elif model == "GPT-OSS-120B":
        return ChatOpenAI(
            model = "openai/gpt-oss-120b:free",
            api_key = OPENROUTER_API_KEY,
            base_url = "https://openrouter.ai/api/v1"
            )
        

def initialize_llm_chain():
    llm_model = select_llm_model()
    prompt = ChatPromptTemplate.from_messages([
        *st.session_state["messages"],
        ("user", "{user_input}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm_model | output_parser
    return chain 



def generate_response(chain, user_input):
    return chain.invoke({"user_input": user_input})


def chat_with_history(chain):

#    for role, message in st.session_state.get("messages", []):
#        st.chat_message(role).markdown(message)

    #display  chat messages。最初は何も入ってないから実行されない
    #st.sessions_state["messages"] = [{"role":, "content":}, {"role":, "content":}] 
    #st.sessions_state["messages"] = [("role", "{role}")///]
    for message in st.session_state["messages"]:
        with st.chat_message(message[0]):
            st.markdown(message[1])

    if user_input := st.chat_input("Say something"):
#        response = generate_response(chain, user_input)
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("ai"): 
        #    response = st.stream(chain.invoke({"user_input": user_input}))
             response = st.write_stream(chain.stream({"user_input": user_input}))



        st.session_state["messages"].append(("user", user_input))
        st.session_state["messages"].append(("ai", response))



def main():
    initialize_app()
    initialize_message()
    chain = initialize_llm_chain()
    chat_with_history(chain)

if __name__ == "__main__":
    main()