import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
import src.db as db

st.write("My info")
# try:
if st.session_state['login']== True:
  
  st.write(f"{st.session_state['account']}님 환영합니다.")
  if st.session_state['admin'] == True:
    st.write("관리자입니다")
  if st.session_state['teacher'] == True:
    # account menu for teacher
    pass
  else: 
    # account menu for student
    pass
  
  # show student info page
  # example
  student_info = db.get_student_info(st.session_state['student_id'])
  # st.write(student_info)
  default_student_info = {
    'account': student_info['account'][0],
    'name': student_info['name'][0],
    'age': student_info['age'][0],
    'grade': student_info['grade'][0],
    'date_joined': student_info['date_joined'][0],
    'last_login': student_info['last_login'][0],
  }
  st.write(default_student_info)
  
  
else:
  st.write("로그인이 필요합니다.")
  clicked = st.button("main")
  if clicked:
    switch_page('home')
    
# except Exception as e:
#   switch_page("home")
