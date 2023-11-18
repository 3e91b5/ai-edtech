import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import openai
import problemset, account
st.set_page_config(page_title = "AI-EdTech")

class EdTechApp:
	def __init__(self):
		self.apps = [] 
		
	def add_app(self, title, function):
		self.apps.append({
			"title": title,
			"function": function
		})
		
	def init_connection():
    		return psycopg2.connect("host=147.47.200.145 dbname=teamdb3 user=team3 password=eduteam3# port=34543")
	
	def gpt_connection():
		api_key = '[AUTH_KEY]'
		return api_key
		
	def run_query(query):
	    try:
	        conn = init_connection()
	        df = pd.read_sql(query, conn)
	    except psycopg2.Error as e:
	        print("DB error: ", e)
	        conn.close()
	    finally:
	        conn.close()
	    return df

	def run_tx(query):
	    try:
	        conn = init_connection()
	        with conn.cursor() as cur:
	            cur.execute(query)
	    except psycopg2.Error as e:
	        print("DB error: ", e)
	        conn.rollback()
	        conn.close()
	    finally:
	        conn.commit()
	        conn.close()
	    return

	def run_gpt(query):
		openai.api_key = gpt_connection()
		messages = [{"role": "", "content": ""}] 
		response = openai.ChatCompletion.create(
			model = 'gpt-',
			messages = messages
		)
		msg = response['choices'][0]['message']['content']
		return msg
		
	def run():
		with st.sidebar:
			app = option_menu(
			menu_title = 'Menu',
			options=['Main', 'Problem-sets', 'Account'],
			icons=['house-fill', 'trophy-fill', 'person-circle'],
			menu_icon='chat-text-fill',
			default_index=1,
			styles={
				"container": {"padding": "5!important", "background-color": 'gray'},
				"icon": {"color": "white", "font-size": "23px"},
				"nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
				"nav-link-selected": {"background-color": "#02ab21"},}
				)
		if app == 'Main':
			with st.form("form1"):
	    			sid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
	    			spwd = st.text_input('Password:', type='password', placeholder="4자리 비밀번호 입력", max_chars=4)
	    			submitted = st.form_submit_button("로그인")
			df = run_query('SELECT * FROM student ORDER BY sid ')
			st.table(df)
		if app == 'Problem-sets':
			problemset.app() 
		if app == 'Account':
			account.app() 
	
	run()
