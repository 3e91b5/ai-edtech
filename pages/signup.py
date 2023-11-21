import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import src.db as db

# def app():

if st.session_state['login'] == False:
    st.write("signup page")
    with st.form("signup"):
        new_pid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
        new_password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)
        submitted = st.form_submit_button("회원가입")
        if submitted:
            if new_pid and new_password:
                print("signup submitted")
                print("  ID: ", new_pid)
                print("  password: ", new_password)
                success = db.add_user(new_pid, new_password)
                if success:
                    st.success("회원가입 성공! 로그인해주세요")
                    switch_page("Home")
                else:
                    st.error("이미 존재하는 ID입니다.")
            else:
                st.error("모든 정보를 입력해주세요")
                # write postgresql query to check if the user_id exists in the database
                
                # if it exists, redirect to login page
else:
    # TODO: redirect to another page
    st.write("이미 로그인중입니다.")
    st.button("Home", on_click=switch_page("main"))




