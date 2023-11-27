import requests
from openai import OpenAI
import streamlit as st
import datetime


def set_apikey(apikey):

    st.session_state["api_key"] = apikey
    # api_key = apikey

def get_apikey():
    return st.session_state["api_key"]



def run_gpt_helloworld():
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=get_apikey(),
	)
    messages = [
        {'role':"assistant", 'content':"You are professional mathematics teacher. As a good and kind teacher, you are teaching a student who is struggling with math. The student is asking you a question. Please answer the question."},
        {"role": "user", "content": f"Hello. I am {st.session_state['sid']}!. Can you introduce yourself using 1 sentence?"}, # this prompt should be improved
    ]
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    response = completion.choices[0].message.content
    
    return response,  client
    
# get the question from student and do prompt engineering for gpt
def default_prompt(question):
    messages = [
        {'role':"assistant", 'content':"You are professional mathematics teacher. As a good and kind teacher, you are teaching a student who is struggling with math. The student is asking you a question. Please answer the question."},
        {"role": "user", "content": question},
    ]
    return messages


def run_gpt(messages, client):
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    response = completion.choices[0].message.content
    return response
