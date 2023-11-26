import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def add_qid(qid):
    st.session_state['qid'] = qid
    switch_page("question")

def question_buttons(problems, item):
    if problems['level'][item] == "high":
        st.write(":fire:" * 3) 
    elif problems['level'][item] == "mid":
        st.write(":fire:" * 2)
    else:
        st.write(":fire:" * 1)

    # 학생이 이미 푼 문제라면 red로 색상 변경 
    if problems['solved'][item] == 1:
        st.button(f"문제 {problems['qid'][item]}", on_click=add_qid, args=f"{problems['qid'][item]}", type = 'primary')    
    else:
        st.button(f"문제 {problems['qid'][item]}", on_click=add_qid, args=f"{problems['qid'][item]}")
