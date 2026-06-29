import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

import requests
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import urlparse

SUMMARIZE_PROMPT = """以下のコンテンツについて内容を300文字程度で分かりやすく要約してください

=========
{content}
=========

日本語で書いてください！
"""

def init_page():
    st.set_page_config(
        page_title = "Website Summarizer",
    )

    st.header("Website Summarizer")
    st.sidebar.title("Options")

def select_model(temperature=0):
    Qwen_a = "Qwen3.5-9b@q8_0"
    Qwen_b = "Qwen3.5-9b@q4_k_m"
    Gemma = "Gemma"
    models = (Qwen_a, Qwen_b, Gemma)

    
    model = st.sidebar.radio("choose a model", models)
    if model == Qwen_a: 
        return ChatOpenAI(
            temperature=temperature,
            model_name = "Local/qwen3.5-9b@q8_0",
            api_key = "llm-studio",
            base_url = "http://192.168.11.40:1234/v1", 
        )
    elif model == Qwen_b:
        return ChatOpenAI(
            temperature=temperature,
            model_name = "Local/qwen3.5-9b@q4_k_m",
            api_key = "llm-studio",
            base_url = "http://192.168.11.40:1234/v1", 
        )
    elif model == "Gemma": 
        return ChatOpenAI(
            temperature=temperature,
            model_name = "google/gemma-4-e4b",
            api_key = "llm-studio",
            base_url = "http://192.168.11.40:1234/v1", 
 
        )
        
    
def init_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages([
        ("user", SUMMARIZE_PROMPT)
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm |output_parser
    return chain

def validate_url(url):
    """URLが有効かどうか判定する関数"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_content(url):
    try: 
        with st.spinner("Fetching Website"):
            response = requests.get(url)
            response.encoding = response.apparent_encoding

            doc = Document(response.text)
            soup = BeautifulSoup(doc.summary(), "html.parser")
            return soup.get_text(strip=True)
    except:
        st.write(traceback.format_exc())
        return None


def main():
    init_page()
    chain = init_chain()


    if url := st.text_input("URL: ", key="input"):
        is_valid_url = validate_url(url)

        if not is_valid_url:
            st.write("please input valid url")
        else:
            if content := get_content(url):
                st.markdown("## SUMMARY")
                st.write_stream(chain.stream({"content": content}))
                st.markdown("---")
                st.markdown("## Origial Test")
                st.write(content)
            else:
                st.markdown("notihin")


if __name__ == "__main__":
    main()






