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
        {"role": "user", "content": f"Hello. I am {st.session_state['student_id']}!. Can you introduce yourself using 1 sentence?"}, # this prompt should be improved
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

def run_gpt_handwritten(url, client):
    completion = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user", 
        "content": [
            {"type": "text", "text": "This is a handwritten answer to a math problem. Encode it into LATEX."},
            {
                "type": "image_url",
                "image_url": {
                "url": url,
                },
            }
        ],
        }
    ],
    )
    return completion.choices[0].message.content

def scored(answer):
    # input은 latex 답안
    # db에 채점 결과 넣는 것 까지. return 따로 없음.
    # db.update_solved(problem_id, student_id, score, ocr_solved)
    return True
