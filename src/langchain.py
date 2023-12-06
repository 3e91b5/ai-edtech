# After installing langchain, you need to run 'openai migrate' command in cli for the first time.
import random
import psycopg2
import streamlit as st
import os
import openai
import psycopg2
import streamlit as st
import pandas as pd
import json
import glob
import openai
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SQLDatabase
from langchain.prompts import ChatPromptTemplate
from langchain.cache import SQLAlchemyCache
from langchain.globals import set_llm_cache
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import LLMChain # These are not working on openai>=1.2.0
from langchain_experimental.sql import SQLDatabaseChain # These are not working on openai>=1.2.0

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

def get_problem(cursor, problem_id):
    query = """
    SELECT
        p.problem_id,
        p.question,
        p.solution,
        p.hint,
        p.level,
        p.step_criteria,
        p.step_score,
        p.competence,
        ARRAY_AGG(DISTINCT k.knowledge_name) AS knowledge,
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
    problem['step_criteria'] = query_data[0][5]
    problem['step_score'] = query_data[0][6]
    problem['competence'] = query_data[0][7]
    problem['knowledge'] = query_data[0][8]
    problem['sub_unit'] = query_data[0][9]
    problem['main_unit'] = query_data[0][10]
    problem['area'] = query_data[0][11]
    
    return problem

def get_student_answer(cursor, student_id, problem_id):
    query = """
    SELECT
        student_answer,
        step_score,
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
    student_answer['step_score'] = query_data[0][1]
    student_answer['feedback'] = query_data[0][2]
    
    return student_answer

def get_system_prompt(problem, student_answer):
    prompt = """
    Mathematics Problem Interactive Feedback Session

    Context: You are a chatbot tasked with discussing a mathematics problem with a student. Your role is to provide interactive feedback on the student's submitted answer, guide them to understand any mistakes, and encourage learning.

    Problem Details:
    - Question: {}
    - Correct Solution: {}
    - Hint for the problem: {}
    - Criteria for each step: {}
    - Score for each step: {}

    Student's Submission:
    - Answer: {}
    - student's score for each step: {}
    - Feedback: {}

    Instructions:
    - Engage in a friendly and supportive conversation with the student.
    - Discuss the student's answer, highlighting what was done well and where improvements can be made.
    - Use the provided hint and correct solution to guide the student towards understanding any errors.
    - Offer constructive suggestions on how to approach similar problems in the future.
    - Encourage the student to ask questions and express any confusion for further clarification.

    """.format(
        # problem['question'], problem['solution'], problem['hint'], 
        # student_answer['student_answer'], student_answer['score'], 
        # student_answer['feedback']
        problem['question'], problem['solution'], problem['hint'],
        problem['step_criteria'], problem['step_score'],
        student_answer['student_answer'], student_answer['step_score'],
        student_answer['feedback']
    )
    
    return prompt

