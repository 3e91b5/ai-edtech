# Import required libraries
import src.gpt as gpt
import src.db as db
import streamlit as st
from streamlit_chat import message
from src.langchain import (
    get_problem, get_student_answer, get_system_prompt, 
    get_or_create_session, save_message, load_chat_history, 
    generate_response, submit)
from langchain.chat_models import ChatOpenAI
import time
from dotenv import load_dotenv


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

# Display the chat history
if st.session_state['generated']:
    # Add First System Message
    for i in range(len(st.session_state['generated'])):
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
        # Display AI response
        message(st.session_state["generated"][i], key=str(i) + '_ai')


    # # 새로운 메시지 추가
    # message(entered_prompt, is_user=True, key=str(len(user_inputs)-1) + '_user')
    # message(output, key=str(len(ai_generated)-1) + '_ai')

    # 입력 필드 초기화
    # st.session_state['prompt_input'] = ""

# Create a text input box for user input
st.text_input('YOU: ', key='prompt_input', on_change=submit)
