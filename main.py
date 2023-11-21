import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page 

import pandas as pd
import time

import src.db as db
# import pages.problemset as problemset, pages.account as account, pages.signup as signup



st.set_page_config(
    page_title = "AI-EdTech",
    initial_sidebar_state = "auto",
    
)

# session state initialization
if 'login' not in st.session_state: # should be changed to more clever way
	print("init session state")
	st.session_state['pid'] = None
	st.session_state['login'] = False
	st.session_state['teacher'] = False




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

def submit_callback(button_name):
    if button_name == '로그인' and pid == "" and password == "":
        pass
    else:
        print(button_name,"submitted", pid, password)

def logout_callback():
    print('logout callback')
    st.session_state['login'] = False
    st.session_state['pid'] = None
    st.session_state['teacher'] = False	



# TODO: main page contents



if st.session_state["login"] == False:
	# login box
	with st.form("home"):
			st.write("Login Page")
			pid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
			password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)

			
			submitted = st.form_submit_button("로그인", on_click=submit_callback('로그인'))
    
			if submitted:
				if pid and password:
					
					login = db.login_user(pid,password)
					if login:
						st.session_state['login'] = True
						st.session_state['pid'] = pid
						st.success("로그인 성공! 3초 뒤 페이지가 이동됩니다.")
						
						# redirect to account page after few seconds
						time.sleep(3)
						switch_page("Account")
					else:
						st.error("ID 혹은 비밀번호를 다시 입력해주세요")
				else:
					st.error("모든 정보를 입력해주세요")
	if st.button("회원가입"):
		switch_page('signup')
else:
    st.write("로그인 중", "ID:", st.session_state["pid"])
    if st.button('로그아웃'):
        logout_callback()
        switch_page('main')
    
    # st.button('로그아웃', on_click=logout_callback()) #왜 안되냐
    

    
# if app == "Home":
# 	with st.form("form1"):
# 		st.write("Login Page")
# 		pid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
# 		password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)

# 		submitted = st.form_submit_button("로그인", on_click=submit_callback('로그인'))
# 		if submitted:
# 			if pid and password:
				
# 				login = db.login_user(pid,password)
# 				if login:
# 					st.success("로그인 성공!")
# 					# redirect to account page after few seconds
# 					switch_page("Account")
# 					pass
					
# 				else:
# 					st.error("ID 혹은 비밀번호를 다시 입력해주세요")
# 			else:
# 				st.error("모든 정보를 입력해주세요")
# 	if st.button("회원가입"):
# 		switch_page('sign-up')
# 		# pid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
# 		# password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)
# 		# if pid == "" or password == "":
# 		# 	st.error("모든 정보를 입력해주세요")
# 		# else:
# 		# 	add_user(pid,password)
# 	# with st.form("form2"):
# 	# 	signup = st.link_button("회원가입")
# 	# 	if signup:
# 	# 		pass
			

# if app == 'Problem-sets':
# 	problemset.app() 
# if app == 'Account':
# 	account.app() 
	
# if app == 'Sign-up':
# 	signup.app()
