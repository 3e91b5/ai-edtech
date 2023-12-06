# Import required libraries
from dotenv import load_dotenv
from itertools import zip_longest
import psycopg2
from psycopg2 import sql
import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import src.db as db
# from src.langchain import get_problem, get_student_answer, get_system_prompt

connection = db.init_connection()
cursor = connection.cursor()

def get_or_create_session(student_id, problem_id):
    """
    Get existing or create a new session for given student_id and problem_id.
    """
    # Check if session exists
    cursor.execute(
        sql.SQL("SELECT Session_ID FROM Chat_DB.Session WHERE Student_ID = %s AND Problem_ID = %s"),
        (student_id, problem_id)
    )
    result = cursor.fetchone()

    # Create a new session if it doesn't exist
    if result:
        session_id = result[0]
    else:
        # 새로운 세션 추가
        cursor.execute(
            sql.SQL("INSERT INTO Chat_DB.Session (Student_ID, Problem_ID) VALUES (%s, %s) RETURNING Session_ID"),
            (student_id, problem_id)
        )
        session_id = cursor.fetchone()[0]
        connection.commit()

    return session_id

# todo: Need to load student_id and problem_id from the student's current problem page session
student_id = 22  # Example student ID
problem_id = 1  # Example problem ID
session_id = get_or_create_session(student_id, problem_id)
print(f"Session ID: {session_id}")

def save_message(session_id, is_student, message):
    """
    Save a message to the Chat_DB.Message table.
    """
    try:
        cursor.execute(
            sql.SQL("INSERT INTO chat_db.Message (session_id, is_Student, Message, Timestamp) VALUES (%s, %s, %s, NOW())"),
            (session_id, is_student, message)
        )
        connection.commit()
    except Exception as e:
        print(f"Error saving message: {e}")
        connection.rollback()

def load_chat_history(session_id):
    """
    Load previous AI-generated and user input messages from the database.
    """
    cursor.execute(
        "SELECT is_Student, Message FROM Chat_DB.Message WHERE Session_ID = %s ORDER BY Timestamp",
        (session_id,)
    )
    ai_messages = []
    user_messages = []
    for is_student, message in cursor.fetchall():
        if is_student:
            user_messages.append(message)
        else:
            ai_messages.append(message)
    return user_messages, ai_messages


# need to make new function to load the problem and student data from the database
# def load_problem_and_student_data(problem_id, student_id):

# Load environment variables
load_dotenv()

# Set streamlit page configuration
st.set_page_config(page_title="Interactive ChatBot")
st.title("Interactive ChatBot")


# Initialize session state variables
if 'generated' not in st.session_state or 'past' not in st.session_state:
    user_inputs, ai_generated = load_chat_history(session_id)
    st.session_state['generated'] = ai_generated  # Store AI generated responses
    st.session_state['past'] = user_inputs  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo"
)

def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        content="You are a helpful AI assistant talking with a human. If you do not know an answer, just say 'I don't know', do not make up an answer.")]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt
    # Save user query to database
    save_message(session_id, True, user_query)

    # Append user query to past queries
    st.session_state.past.append(user_query)
    
    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)
    # Save AI response to database
    save_message(session_id, False, output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))

# Create a text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit)
