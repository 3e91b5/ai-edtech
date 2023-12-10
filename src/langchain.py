import random
import psycopg2
import streamlit as st
import os
import openai
import psycopg2
from psycopg2 import sql
from itertools import zip_longest
import streamlit as st
import pandas as pd
import json
import glob
import openai
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SQLDatabase
from langchain.prompts import ChatPromptTemplate
from langchain.cache import SQLAlchemyCache
from langchain.globals import set_llm_cache
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from src.db import check_connection

def init_db(include_tables = []):
    """
    Initialize a SQL database db object for langchain using the credentials stored in st.secrets.

    Returns:
    db (SQLDatabase): The SQL database object.
    pg_uri (str): The PostgreSQL URI used for the connection.
    """

    # Retrieve the credentials from st.secrets
    user = st.secrets['username']
    password = st.secrets['password']
    host = st.secrets['host']
    port = st.secrets['port']
    database = st.secrets['database']
    
    # Create the PostgreSQL URI
    pg_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    
    # Create the SQLDatabase object
    if include_tables == []:    
        db = SQLDatabase.from_uri(pg_uri)
    else:
        db = SQLDatabase.from_uri(pg_uri, include_tables=include_tables,sample_rows_in_table_info=2)
    
    return db, pg_uri

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

# Get the problem from DB
def get_problem(problem_id):
    cursor = check_connection()
    query = """
    SELECT
        p.problem_id,
        p.question,
        p.solution,
        p.hint,
        p.level,
        p.knowledge_score,
        ARRAY_AGG(DISTINCT su.sub_unit_name) AS sub_unit,
        ARRAY_AGG(DISTINCT mu.main_unit_name) AS main_unit,
        ARRAY_AGG(DISTINCT a.area_name) AS area
    FROM
        knowledge_map_db.problem p
    INNER JOIN knowledge_map_db.knowledge_problem kp
        ON p.problem_id = kp.problem_id
    INNER JOIN knowledge_map_db.knowledge k
        ON kp.knowledge_id = k.knowledge_id
    INNER JOIN knowledge_map_db.sub_unit su
        ON k.sub_unit_id = su.sub_unit_id
    INNER JOIN knowledge_map_db.main_unit mu
        ON su.main_unit_id = mu.main_unit_id
    INNER JOIN knowledge_map_db.area a
        ON mu.area_id = a.area_id
    WHERE
        p.problem_id = {}
    GROUP BY
        p.problem_id;
    """.format(problem_id)

    cursor.execute(query)
    query_data = cursor.fetchall()

    # make problem dictionary
    problem = {}
    problem['problem_id'] = query_data[0][0]
    problem['question'] = query_data[0][1]
    problem['solution'] = query_data[0][2]
    problem['hint'] = query_data[0][3]
    problem['level'] = query_data[0][4]
    problem['knowledge_score'] = query_data[0][5]
    problem['sub_unit'] = query_data[0][6]
    problem['main_unit'] = query_data[0][7]
    problem['area'] = query_data[0][8]
    
    return problem

# Get the student answer from DB
def get_student_answer(student_id, problem_id):
    cursor = check_connection()

    query = """
    SELECT
        student_answer,
        knowledge_score,
        feedback
    FROM
        Student_DB.Problem_Progress
    WHERE
        Student_ID = {} AND
        Problem_ID = {}
    ORDER BY
        Timestamp DESC
    LIMIT 1;
    """.format(student_id, problem_id)

    cursor.execute(query)
    query_data = cursor.fetchall()

    # make problem dictionary
    student_answer = {}
    student_answer['student_answer'] = query_data[0][0]
    student_answer['knowledge_score'] = query_data[0][1]
    student_answer['feedback'] = query_data[0][2]
    
    return student_answer

# Make system prompt
def get_system_prompt(problem, student_answer):
    prompt = """
    Mathematics Problem Interactive Feedback Session

    Context: You are a chatbot tasked with discussing a mathematics problem with a student. Your role is to provide interactive feedback on the student's submitted answer, guide them to understand any mistakes, and encourage learning.

    Problem Details:
    - Question: {}
    - Correct Solution: {}
    - Hint for the problem: {}
    - Related knowledge and its score: {}
    - Related high-school math unit: {}
    
    Student's Submission:
    - Answer: {}
    - student's score for each knowledge: {}
    - Feedback: {}

    Instructions:
    - During the conversation, you should use Korean language.
    - Engage in a friendly and supportive conversation with the student.
    - Discuss the student's answer, highlighting what was done well and where improvements can be made.
    - Use the provided hint and correct solution to guide the student towards understanding any errors.
    - Offer constructive suggestions on how to approach similar problems in the future.
    - Encourage the student to ask questions and express any confusion for further clarification.

    """.format(
        problem['question'], problem['solution'], problem['hint'],
        problem['knowledge_score'], problem['main_unit'],
        student_answer['student_answer'], student_answer['knowledge_score'],
        student_answer['feedback']
    )
    
    return prompt

# Get or create session for chatbot
def get_or_create_session(student_id, problem_id):
    cursor = check_connection()
    """
    Get existing or create a new session for given student_id and problem_id.
    """
    # Check if session exists
    cursor.execute(
        sql.SQL("SELECT Session_ID FROM Chat_DB.Session WHERE Student_ID = %s AND Problem_ID = %s"),
        (int(student_id), int(problem_id))
    )
    result = cursor.fetchone()

    # Create a new session if it doesn't exist
    if result:
        session_id = result[0]
    else:
        # 새로운 세션 추가
        cursor.execute(
            sql.SQL("INSERT INTO Chat_DB.Session (Student_ID, Problem_ID) VALUES (%s, %s) RETURNING Session_ID"),
            (int(student_id), int(problem_id))
        )
        session_id = cursor.fetchone()[0]
        st.session_state.connection.commit()

    return session_id

# Save message to DB
def save_message(session_id, is_student, message):
    cursor = check_connection()
    """
    Save a message to the Chat_DB.Message table.
    """
    print(f"Saving message: {message}")
    try:
        cursor.execute(
            sql.SQL("INSERT INTO chat_db.Message (session_id, is_Student, Message, Timestamp) VALUES (%s, %s, %s, NOW())"),
            (session_id, is_student, message)
        )
        st.session_state.connection.commit()
    except Exception as e:
        print(f"Error saving message: {e}")
        st.session_state.connection.rollback()
    finally:
        cursor.close()


# Load chat history from DB
def load_chat_history(session_id):
    cursor = check_connection()
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

# Build a list of messages including system, human and AI messages.
def build_message_list(system_prompt):
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        content=system_prompt)]  # Add system message

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages

# Generate AI response using the ChatOpenAI model.
def generate_response(chat, system_prompt):
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list(system_prompt)

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content

# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""

