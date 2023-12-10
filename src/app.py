import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def add_problem_id(problem_id):
    st.session_state['problem_id'] = problem_id
    switch_page("question")

def question_buttons(problems, item):
    if problems['level'][item] >= 4:
        st.write(":fire:" * 3) 
    elif problems['level'][item] >= 2:
        st.write(":fire:" * 2)
    else:
        st.write(":fire:" * 1)

    # 학생이 이미 푼 문제라면 red로 색상 변경 
    if problems['solved'][item] == 1:
        # clicked = st.button(f"문제 {problems['problem_id'][item]}", on_click=add_problem_id, args=f"{problems['problem_id'][item]}", type = 'primary')    
        clicked = st.button(f"문제 {problems['problem_id'][item]}", args=f"{problems['problem_id'][item]}", type = 'primary')    
        if clicked:
            add_problem_id(problems['problem_id'][item])
    else:
        # st.button(f"문제 {problems['problem_id'][item]}", on_click=add_problem_id, args=f"{problems['problem_id'][item]}")
        st.button(f"문제 {problems['problem_id'][item]}",  args=f"{problems['problem_id'][item]}")
        if clicked:
            add_problem_id(problems['problem_id'][item])
