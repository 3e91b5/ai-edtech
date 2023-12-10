# Import required libraries
# from dotenv import load_dotenv
import src.gpt as gpt
import src.db as db
from itertools import zip_longest
import psycopg2
import streamlit as st
from streamlit_chat import message
# import src.db as db
from src.langchain import (
    get_problem, get_student_answer, get_system_prompt, 
    get_or_create_session, save_message, load_chat_history, 
    generate_response, submit)
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from streamlit_extras.switch_page_button import switch_page
import glob
import json
import os
import random
import time


# def interactive_chatbot():
# # todo: Need to load st.session_state["student_id"] and st.session_state["problem_id"] from the student's current problem page session
st.session_state["student_id"] = 12345678  # Example student ID
st.session_state["problem_id"] = 1  # Example problem ID
# st.session_state["student_id"] = st.session_state['st.session_state["student_id"]']
# st.session_state["problem_id"] = st.session_state['st.session_state["problem_id"]']

# check the existence of connection and cursor 
if 'cursor' not in st.session_state:
    if 'connection' not in st.session_state:
        connection = db.init_connection()
    cursor = connection.cursor()

if 'session_id' not in st.session_state:
    st.session_state["session_id"] = get_or_create_session(connection, cursor, st.session_state["student_id"], st.session_state["problem_id"])

# get problem, student answer from DB and make system prompt
if 'problem' not in st.session_state:
    st.session_state["problem"] = get_problem(cursor, st.session_state["problem_id"])

if 'student_answer' not in st.session_state:
    st.session_state["student_answer"] = get_student_answer(cursor, st.session_state["student_id"], st.session_state["problem_id"])

if 'system_prompt' not in st.session_state:
    st.session_state["system_prompt"] = get_system_prompt(st.session_state["problem"], st.session_state["student_answer"])

# need to make new function to load the problem and student data from the database
# def load_problem_and_student_data(st.session_state["problem_id"], st.session_state["student_id"]):

# # Load environment variables
# load_dotenv()

# Set streamlit page configuration
st.set_page_config(page_title="Interactive ChatBot")
st.title("Interactive ChatBot")

# Display the problem and student answer as markdown 
st.write("Problem: ", st.session_state["problem"]['question'])
st.write("Student Answer: ", st.session_state["student_answer"]['student_answer'])
st.write("Feedback: ", st.session_state["student_answer"]['feedback'])

# Initialize session state variables
if 'generated' not in st.session_state or 'past' not in st.session_state:
    user_inputs, ai_generated = load_chat_history(cursor, st.session_state["session_id"])
    print(user_inputs)
    print(ai_generated)
    st.session_state['generated'] = ai_generated  # Store AI generated responses
    st.session_state['past'] = user_inputs  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
if 'chat' not in st.session_state:
    chat = ChatOpenAI(
        # client = st.session_state['gpt_client'],
        api_key= st.session_state['api_key'],
        temperature=0.3,
        model_name="gpt-4-1106-preview"
    )

if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt
    # Save user query to database
    save_message(connection, cursor, st.session_state["session_id"], True, user_query)

    # Append user query to past queries
    st.session_state.past.append(user_query)
    
    # Generate response
    output = generate_response(chat, st.session_state["system_prompt"])

    # Append AI response to generated responses
    st.session_state.generated.append(output)
    # Save AI response to database
    save_message(connection, cursor, st.session_state["session_id"], False, output)

first_message = "안녕하세요. 당신의 학습을 도와줄 인공지능 챗봇입니다. 위의 피드백을 참고하여 어떤 도움을 얻고 싶으신가요?"
message(first_message, key='first_message')

# Display the chat history
if st.session_state['generated']:
    # Add First System Message
    for i in range(len(st.session_state['generated'])):
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
        # Display AI response
        message(st.session_state["generated"][i], key=str(i) + '_ai')

# Create a text input box for user input
st.text_input('YOU: ', key='prompt_input', on_change=submit)


# if 'login' in st.session_state:
#     if st.session_state['login'] == True:
#         interactive_chatbot()
        
            
#     else:
#         st.write("로그인이 필요한 서비스입니다.")
#         clicked = st.button("main")
#         if clicked:
#             switch_page("home")        
# else:
#     st.write("로그인이 필요한 서비스입니다.")
#     clicked = st.button("main")
#     if clicked:
#         switch_page("home")
