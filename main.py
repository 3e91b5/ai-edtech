import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page 
import datetime
import pandas as pd
import src.db as db
import pages.menu as menu, pages.practice as practice, pages.graded as graded, pages.performance as performance, pages.info as info, pages.admin as admin, pages.signup as signup, pages.chatbot as chatbot
from st_pages import show_pages_from_config, add_page_title
add_page_title()
show_pages_from_config()

st.set_page_config(
    page_title = "AI-EdTech",
    initial_sidebar_state = "auto",
    
)

# session state initialization
if 'login' not in st.session_state: # should be changed to more clever way
	print(datetime.datetime.now(), "init session state")
	st.session_state['login'] = False # whether the user is logged in or not
	st.session_state['admin'] = False # whether the user is an admin or not
	st.session_state['student_id'] = 12345678
	st.session_state['problem_id'] = 1 

def __init__(self):
	self.apps = []
	
def add_app(self, title, function):
	self.apps.append({
		"title": title,
		"function": function
	})

# callback function for submit button to write log
def submit_callback(button_name):
    if button_name == '로그인' and student_id == "" and password == "":
        pass
    else:
        print(datetime.datetime.now(), button_name,"submitted", student_id, password)

def logout_callback():
	print(datetime.datetime.now(), 'logout callback')
	st.session_state['login'] = False
	st.session_state['admin'] = False

# TODO: main page contents
st.title("AI-EdTech")
st.header("My header")
st.subheader("My subheader")
link = '[GitHub](https://github.com/jean-jsj/ai-edtech/tree/jwhong)'

# the main page
if st.session_state["login"] == False:	# if not logged in
	# login box
	with st.form("home"):
			st.write("Login Page")
			student_id = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
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
				if student_id and password:
					
					login = db.login_user(student_id,password)
					if login:
						st.session_state['login'] = True
						st.session_state['student_id'] = student_id
						if db.is_admin(student_id):
							st.session_state['admin'] = True
						st.success("로그인 중")
    
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
    st.write("로그인 중", "ID:", st.session_state["student_id"])
	# show logout button
    if st.button('로그아웃'):
        logout_callback()
        switch_page('main')
    
    # st.button('로그아웃', on_click=logout_callback()) #왜 안되냐
