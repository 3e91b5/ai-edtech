import streamlit as st
# from streamlit_option_menu import option_menu
import time
from streamlit_extras.switch_page_button import switch_page 
import datetime
import pandas as pd
import src.db as db
from st_pages import Page, Section, show_pages

st.set_page_config(
    page_title = "AI-EdTech",
    initial_sidebar_state = "auto",  
)

show_pages(
    [
        Page("main.py", "Home", ':classical_building:'),
        Section(name="My Page", icon=':information_desk_person:'),
        Page("pages/info.py", "My Info"),
        Page("pages/performance.py", "My Performance"),
        Page("pages/admin.py", "Admin"),
        Section(name="Math Drill", icon=':books:'),
        Page("pages/menu.py", "Menu"),
        Page("pages/practice.py", "Question"),
        Page("pages/graded.py", "Graded Result"),
        Page("pages/chatbot.py", "Chat with ai", ':question:')
    ]
)

# when the user first logs in, session_state is initialized
# when the user logs out, session_state is reset
def session_state_reset():
	#student info
	st.session_state['student_id'] = None
	st.session_state['account'] = None
	st.session_state['name'] = None
	st.session_state['login'] = False
	st.session_state['teacher'] = False
	st.session_state['admin'] = False
	st.session_state['problem_id'] = None 
	
	# chatbot
	st.session_state['api_key'] = None
	st.session_state['openai_model'] = None
	st.session_state['message'] = []
	st.session_state['gpt_session'] = False
	st.session_state['gpt_client'] = None

# after login, session_state is initialized by student info from the database
def session_state_login_init(account):
	student_info = db.get_student_info_by_account(account)
	student_id = student_info['student_id'][0]

	st.session_state['login'] = True
	st.session_state['account'] = account
	st.session_state['name'] = student_info['name'][0]
	st.session_state['student_id'] = student_id
	if db.is_admin(student_id):
		st.session_state['admin'] = True
        
# session state initialization
if 'login' not in st.session_state: # should be changed to more clever way
	print(datetime.datetime.now(), "init session state")
	session_state_reset()

def __init__(self):
	self.apps = []
	
def add_app(self, title, function):
	self.apps.append({
		"title": title,
		"function": function
	})

def logout_callback():
    print(datetime.datetime.now(), 'logout callback')
    session_state_reset()

# TODO: main page contents
st.title("AI-EdTech")
st.header("My header")
st.subheader("My subheader")
link = '[GitHub](https://github.com/jean-jsj/ai-edtech/)'
st.markdown(link, unsafe_allow_html=True)

# the main page
if st.session_state["login"] == False:	# if not logged in
	# login box
	with st.form("main"):
			st.write("Login Page")
			account = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
			password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)			
			submitted = st.form_submit_button("로그인")
    
			# if login button is clicked,
			# 1. check whether student_id and password are not empty
			# 2. check whether (student_id, password) pair is in the database (in function db.login_user)
			# 3. if yes, 
			#		initialize session_state by calling session_state_login_init(student_id)
			# 4. switch page to info page (default page)

			if submitted:
				if account and password:
					
					login = db.login_user(account, password)
					if login:
						session_state_login_init(account)
						st.success("로그인 중")
						
						time.sleep(1) # redirect to info page after few seconds
						switch_page('my info')
    
					else: # if login fails
						st.error("ID 혹은 비밀번호를 다시 입력해주세요")
				else: # if student_id or password is empty
					st.error("모든 정보를 입력해주세요")
	if st.button("회원가입"):
		switch_page('signup')


else: # if logged in
    
	# show login status
    st.write("로그인 중", "ID:", st.session_state["name"])
	# show logout button
    if st.button('로그아웃'):
        logout_callback()
        switch_page('home')
