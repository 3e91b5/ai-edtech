# Import required libraries
from itertools import zip_longest
import psycopg2
import streamlit as st
from streamlit_chat import message
import src.db as db
import src.gpt as gpt

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
from dotenv import load_dotenv


# Define the function to run a single chat interaction with the given chat model with prompt
def langchain_single_chat(chat, system_message, human_message):
  """
  Run a single chat interaction with the given chat model.

  Args:
  chat (ChatOpenAI): The chat model.
  system_message (SystemMessage): The system message to send to the chat model.
  human_message (HumanMessage): The human message to send to the chat model.

  Returns:
  response (AIMessage): The response from the chat model.
  """
  # define the messages
  messages = [SystemMessage(content=system_message), HumanMessage(content=human_message)]
  # get the response from the chat model
  response = chat(messages)
  # return the response as a string
  return response.content

# UPDATE DATA -> knowledge_map_db.problem
def insert_problem():
    # Initialize chat models
    api_key = gpt.get_apikey()
    gpt_4 = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.3, api_key=api_key)
    gpt_3 = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.3, api_key=api_key)
    
    # get all files in the nested directory ./MATH/ and shuffle
    files = glob.glob("./MATH/" + "**/*.json", recursive=True)
    random.shuffle(files)

    # Load a json file and print
    for file_path in files[:300]:
        with open(file_path) as f:
            raw_data = json.load(f)
            raw_data = str(raw_data)
            print(raw_data)
            isHighSchoolLevel = langchain_single_chat(gpt_4, gpt.templates["high_school"], raw_data)
            print("isHighSchoolLevel:", isHighSchoolLevel)

            if isHighSchoolLevel == "1":
                process_response = langchain_single_chat(gpt_4, gpt.templates["post_process"], raw_data)
                print("processed data:", process_response)
                insert_problem_query = langchain_single_chat(gpt_3, gpt.templates["insert_problem"], f"{process_response}")
                print("insert_problem_query:", insert_problem_query)
# Load environment variables
load_dotenv()

# initialize session_state
def init_page_variables(student_id, problem_id):
    # Generate or Load session_id
    st.write("student_id: ", student_id, "problem_id: ", problem_id)
    session_id = get_or_create_session(student_id, problem_id)
    # Load problem, student answer, system prompt
    problem = get_problem(problem_id)
    student_answer = get_student_answer(student_id, problem_id)
    system_prompt = get_system_prompt(problem, student_answer)

    # initialize chat object
    chat = ChatOpenAI(
        api_key=st.session_state['api_key'],
        temperature=0.3,
        model_name="gpt-4-1106-preview"
    )

    return session_id, problem, student_answer, system_prompt, chat

if 'connection' not in st.session_state:
    st.session_state.connection = db.init_connection()

# student_id와 problem_id가 존재하는지 확인하고 설정
if "student_id" not in st.session_state:
    st.session_state["student_id"] = 12345678  # 예시 학생 ID

if "problem_id" not in st.session_state or st.session_state["problem_id"] is None:
    st.session_state["problem_id"] = 1  # 예시 문제 ID

# 페이지 설정
st.set_page_config(page_title="Interactive ChatBot")
st.title("Interactive ChatBot")

# 페이지 변수 초기화 함수 호출
session_id, problem, student_answer, system_prompt, chat = init_page_variables(st.session_state['student_id'], st.session_state['problem_id'])

# 문제, 학생의 답변, 피드백 표시
st.write("Problem: ", problem['question'])
st.write("Student Answer: ", student_answer['student_answer'])
st.write("Feedback: ", student_answer['feedback'])

# 채팅 기록 불러오기
if 'generated' not in st.session_state or 'past' not in st.session_state:
    user_inputs, ai_generated = load_chat_history(session_id)
    st.session_state['generated'] = ai_generated  # Store AI generated responses
    st.session_state['past'] = user_inputs  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

if st.session_state.entered_prompt != "":
    # Get user input
    user_query = st.session_state.entered_prompt
    # Save user input to database
    save_message(session_id, True, user_query)
    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate AI response
    output = generate_response(chat, system_prompt)

    # Append AI response to generated responses
    st.session_state.generated.append(output)
    
    # Save AI response to database
    save_message(session_id, False, output)

    # Commit changes to database
    st.session_state.connection.commit()


# 채팅 인터페이스
first_message = "안녕하세요. 당신의 학습을 도와줄 인공지능 챗봇입니다. 위의 피드백을 참고하여 어떤 도움을 얻고 싶으신가요?"
message(first_message, key='first_message')

                
result = db.run_query(insert_problem_query)
    
    # # Conduct insert query on the database
    # try:
    #     cursor = connection.cursor()
    #     cursor.execute(insert_problem_query)
    # except (Exception, psycopg2.Error) as error:
    #     print("Error while connecting to PostgreSQL", error)
    #     connection.rollback()
    # finally:
    #     cursor.close()
    #     connection.commit()
# delete the file to avoid duplication
os.remove(file_path)

image_3 = "/content/answer2.png"

def grade_answer(student_id, problem_id):
    # Initialize chat models
    api_key = gpt.get_apikey()
    gpt_4 = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.3, api_key=api_key)
    gpt_3 = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.3, api_key=api_key)
    
    question, knowledge = get_problem(problem_id)
    
    # get image_path from local server's content folder
    image_path_no_extension = 'content/' + str(student_id) +'_'+str(problem_id)
    for ext in ['png', 'jpg', 'jpeg']:
        if os.path.exists(image_path_no_extension + '.' + ext):
            image_path = image_path_no_extension + '.' + ext
            break
        
    if not os.path.exists(image_path):
        print("No image file found")
        st.error("No image file found")
        return
    
    student_answer = gpt.answer_to_latex(image_path) 

    template_knowledge = PromptTemplate(
        input_variables=[f"{question}", f"{knowledge}"],
        template=gpt.graded_result["knowledge_score"]
    )
    prompt_knowledge = template_knowledge.format(question = question, knowledge = knowledge)

    template_feedback = PromptTemplate(
        input_variables=[f"{question}"],
        template=gpt.graded_result["feedback"]
    )
    prompt_feedback = template_feedback.format(question = question)

    knowledge_score = langchain_single_chat(gpt_4, prompt_knowledge, f"{student_answer}")
    feedback = langchain_single_chat(gpt_4, prompt_feedback, f"{student_answer}")
    answer_dct = {
    "student_answer": student_answer,
    "knowledge_score": knowledge_score,
    "feedback": feedback
    }
    print("answer_dct: ", answer_dct)

    insert_answer_query = langchain_single_chat(gpt_3, gpt.templates["insert_problem"], f"{answer_dct}")

    result = db.run_tx(insert_answer_query)
    # try:
    #     cursor = connection.cursor()
    #     cursor.execute(insert_answer_query)
    # except (Exception, psycopg2.Error) as error:
    #     print("Error while connecting to PostgreSQL", error)
    #     connection.rollback()
    # finally:
    #     cursor.close()
    #     connection.commit()
    # return

def interactive_chatbot():
    # # todo: Need to load student_id and problem_id from the student's current problem page session
    # student_id = 12345678  # Example student ID
    # problem_id = 1  # Example problem ID
    student_id = st.session_state['student_id']
    problem_id = st.session_state['problem_id']

    # check the existence of connection and cursor 
    if 'cursor' not in st.session_state:
        if 'connection' not in st.session_state:
            connection = db.init_connection()
        cursor = connection.cursor()

    if 'session_id' not in st.session_state:
        session_id = get_or_create_session(connection, cursor, student_id, problem_id)
        print(f"Session ID: {session_id}")

    # get problem, student answer from DB and make system prompt
    if 'system_prompt' not in st.session_state:
        problem = get_problem(cursor, problem_id)
        student_answer = get_student_answer(cursor, student_id, problem_id)
        # get system prompt
        system_prompt = get_system_prompt(problem, student_answer)

    # need to make new function to load the problem and student data from the database
    # def load_problem_and_student_data(problem_id, student_id):

    # # Load environment variables
    # load_dotenv()

    # Set streamlit page configuration
    st.set_page_config(page_title="Interactive ChatBot")
    st.title("Interactive ChatBot")

    # Display the problem and student answer as markdown 
    st.write("Problem: ", problem['question'])
    st.write("Student Answer: ", student_answer['student_answer'])
    st.write("Feedback: ", student_answer['feedback'])

    # Initialize session state variables
    if 'generated' not in st.session_state or 'past' not in st.session_state:
        user_inputs, ai_generated = load_chat_history(cursor, session_id)
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
        save_message(connection, cursor, session_id, True, user_query)

        # Append user query to past queries
        st.session_state.past.append(user_query)
        
        # Generate response
        output = generate_response(chat, system_prompt)

        # Append AI response to generated responses
        st.session_state.generated.append(output)
        # Save AI response to database
        save_message(connection, cursor, session_id, False, output)

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



if 'login' in st.session_state:
    if st.session_state['login'] == True:
        interactive_chatbot()
        
            
    else:
        st.write("로그인이 필요한 서비스입니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("home")        
else:
    st.write("로그인이 필요한 서비스입니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")

    # # 새로운 메시지 추가
    # message(entered_prompt, is_user=True, key=str(len(user_inputs)-1) + '_user')
    # message(output, key=str(len(ai_generated)-1) + '_ai')

    # 입력 필드 초기화
    # st.session_state['prompt_input'] = ""

# Create a text input box for user input
st.text_input('YOU: ', key='prompt_input', on_change=submit)
