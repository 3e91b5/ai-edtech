import streamlit as st
import pandas as pd
import psycopg2
from streamlit_option_menu import option_menu
import problemset, account
st.set_page_config(page_title = "AI-EdTech")

class MultiApp:
	def __init__(self):
		self.apps = [] 
		
	def add_app(self, title, function):
		self.apps.append({
			"title": title,
			"function": function
		})
		
	def init_connection():
    		return psycopg2.connect("host=147.47.200.145 dbname=DB이름 user=유저명 password=비밀번호 port=34543")

	def run_query(query):
	    try:
	        conn = init_connection()
	        df = pd.read_sql(query,conn)
	    except psycopg2.Error as e:
	        # 데이터베이스 에러 처리
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
	        # 데이터베이스 에러 처리
	        print("DB error: ", e)
	        conn.rollback()
	        conn.close()
	    finally:
	        conn.commit()
	        conn.close()
	    return
		
	def run():
		with st.sidebar:
			app = option_menu(
			menu_title = 'Menu',
			options=['Main', 'Problem-sets', 'Account'],
			icons=['house-fill', 'trophy-fill', 'person-circle'],
			menu_icon='chat-text-fill',
			default_index=1,
			styles={
				"container": {"padding": "5!important", "background-color": 'black'},
				"icon": {"color": "white", "font-size": "23px"},
				"nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
				"nav-link-selected": {"background-color": "#02ab21"},}
				)
		st.subheader("로그인")
		with st.form("form1"):
    			sid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
    			spwd = st.text_input('Password:', type='password', max_chars=4, help='4자리 비밀번호 입력')
    			submitted = st.form_submit_button("로그인")

    # run the app function inside the main.py file
		if app == 'Problem-sets':
			problemset.app() 
		if app == 'Account':
			account.app() 
	
	run()
