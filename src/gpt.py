import requests
from openai import OpenAI
import streamlit as st
import datetime


def set_apikey(apikey):

    st.session_state["api_key"] = apikey

def get_apikey():
    return st.session_state["api_key"]


# run run_gpt_helloworld() when the user first submit gpt api key
def run_gpt_helloworld():
    client = OpenAI(
    api_key=get_apikey(),
	)
    messages = [
        {'role':"assistant", 'content':"You are professional mathematics teacher. As a good and kind teacher, you are teaching a student who is struggling with math. The student is asking you a question. Please answer the question."},
        {"role": "user", "content": f"Hello. I am {st.session_state['student_id']}! Please answer using 1 sentence include my name."}, # this prompt should be improved
    ]
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    response = completion.choices[0].message.content
    
    return response,  client # TODO: return client can maintain the chat session and remember the context?
    
# get the question from student and do prompt engineering for gpt
def default_prompt(question):
    messages = [
        {'role':"assistant", 'content':"You are professional mathematics teacher. As a good and kind teacher, you are teaching a student who is struggling with math. The student is asking you a question. Please answer the question."},
        {"role": "user", "content": question},
    ]
    return messages

# prompting for student's 1 time question
def prompt_question(question):
    # TODO
    messages = [{}]
    return messages

# prompting for student's interactive communication
def prompt_communication(question):
    # TODO
    messages = [{}]
    return messages


# using prompted messages, run gpt and get the response
def run_gpt(messages, client):
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    response = completion.choices[0].message.content
    return response

# function for sending handwritten message and get latex to gpt-4-vision model
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
