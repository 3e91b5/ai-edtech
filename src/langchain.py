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
