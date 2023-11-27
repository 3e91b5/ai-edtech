import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page 
import datetime
import pandas as pd
import time

import src.db as db
import pages.menu as menu, pages.practice as practice, pages.graded as graded, pages.performance as performance



st.set_page_config(
    page_title = "AI-EdTech",
    initial_sidebar_state = "auto",
    
)

def session_state_reset():
	st.session_state['sid'] = None
	st.session_state['login'] = False
	st.session_state['teacher'] = False
	st.session_state['admin'] = False
	st.session_state['api_key'] = None
	st.session_state['gpt_session'] = False
	st.session_state['gpt_client'] = None

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

# with st.sidebar:
# 	app = option_menu(
# 	menu_title = 'Menu',
# 	options=['Home', 'Problem-sets', 'Account', 'Sign-up'],
# 	icons=['house-fill', 'trophy-fill', 'person-circle', 'person-plus-fill'],
# 	menu_icon='chat-text-fill',
# 	default_index=1,
# 	styles={
# 		"container": {"padding": "5!important", "background-color": 'gray'},
# 		"icon": {"color": "white", "font-size": "23px"},
# 		"nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
# 		"nav-link-selected": {"background-color": "#02ab21"},}
# 		)

# callback function for submit button to write log
def submit_callback(button_name):
    if button_name == '로그인' and sid == "" and password == "":
        pass
    else:
        print(datetime.datetime.now(), button_name,"submitted", sid, password)

def logout_callback():
    print(datetime.datetime.now(), 'logout callback')
    session_state_reset()



# TODO: main page contents
st.title("AI-EdTech")
st.header("My header")
st.subheader("My subheader")
link = '[GitHub](https://github.com/jean-jsj/ai-edtech/tree/jhkim)'
st.markdown(link, unsafe_allow_html=True)
# st.link_button("Github", "https://github.com/jean-jsj/ai-edtech/tree/jhkim")

# the main page
if st.session_state["login"] == False:	# if not logged in
	# login box
	with st.form("home"):
			st.write("Login Page")
			sid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
			password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)			
			submitted = st.form_submit_button("로그인", on_click=submit_callback('로그인'))
    
			# if login button is clicked,
			# 1. check whether sid and password are not empty
			# 2. check whether (sid, password) pair is in the database (in funtion db.login_user)
			# 3. if yes, 
			#		set session_state['login'] to True, 
			# 		session_state['sid'] to user's sid,
			#		session_state['teacher'] to True if the user is a teacher, 
			#		and session_state['admin'] to True if the user is an admin  
			# 4. switch page to account page (default page)

			if submitted:
				if sid and password:
					
					login = db.login_user(sid,password)
					if login:
						st.session_state['login'] = True
						st.session_state['sid'] = sid
						if db.is_admin(sid):
							st.session_state['admin'] = True
						st.success("로그인 중.")
    
						# progress bar
						# progress_text = "Please wait."
						# my_bar = st.progress(0, text = progress_text)
						# for percent_complete in range(100):
						# 	time.sleep(0.01)
						# 	my_bar.progress(percent_complete + 1, text = progress_text)
						# my_bar.empty()
    
    
						# redirect to account page after few seconds
						time.sleep(1)
						
						switch_page("Account")
    
					else: # if login fails
						st.error("ID 혹은 비밀번호를 다시 입력해주세요")
				else: # if sid or password is empty
					st.error("모든 정보를 입력해주세요")
	if st.button("회원가입"):
		switch_page('signup')
else: # if logged in
    
	# show login status
    st.write("로그인 중", "ID:", st.session_state["sid"])
	# show logout button
    if st.button('로그아웃'):
        logout_callback()
        switch_page('main')
    
    # st.button('로그아웃', on_click=logout_callback()) #왜 안되냐
    

    