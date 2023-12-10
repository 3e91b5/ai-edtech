
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# import pandas as pd
import src.db as db
import src.app as app

### 화면 구성
if 'login' in st.session_state:
    if st.session_state['login'] == True:
        student_id = st.session_state['student_id']
        grade = db.get_student_grade(student_id)

        main_units = db.get_main_unit_name(grade)
        sub_units = db.get_sub_unit_name(grade)
        knowledges = db.get_knowledge_name(grade)

        ### 화면 구성

        st.header("학습메뉴")
        col1, padding, col2, col3, col4, col5 = st.columns([3,1,2,2,2,2])
        with col1:

            main_unit = st.selectbox(
                "대단원을 선택해주세요",
                main_units,
                index = None,
                placeholder = "단원명",
                )

            sub_unit = st.selectbox(
                "소단원을 선택해주세요",
                sub_units,
                index = None,
                placeholder = "단원명",
                )

            knowledge = st.selectbox(
                "지식요소를 선택해주세요",
                knowledges,
                index = None,
                placeholder = "단원명",
                )

        if knowledge:
            knowledge_id = db.get_knowledge_id(knowledge)
            problems = db.get_problem_list(knowledge_id)
            problems['solved'] = db.get_history(problems, student_id)
            for item in range(len(problems['problem_id'])):
                if item < 3:
                    with col2:
                        app.question_buttons(problems, item)
                elif (item >= 3 and item < 6):
                    with col3:
                        app.question_buttons(problems, item)
                elif (item >= 6 and item < 9):
                    with col4:
                        app.question_buttons(problems, item)
                else:
                    with col5:
                        app.question_buttons(problems, item)
        else:
            st.write("대단원, 소단원, 지식요소를 전부 선택해주세요.")
    else:
        st.write("로그인이 필요합니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("home")
else:
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")