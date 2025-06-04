import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Gemini Chat Assistant",
    page_icon="🤖",
    layout="centered"
)

@st.cache_resource
def init_gemini():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-1.5-flash')

model = init_gemini()
st.title("🤖 Gemini Chat Assistant")
st.write("Chat with Google's Gemini AI model")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role":"user","content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
             response = model.generate_content(prompt)
             st.markdown(response.text)

             st.session_state.messages.append({"role":"assistant","content": response.text})
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role":"assistant", "content": error_msg})

with st.sidebar:
    st.header("Options")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()