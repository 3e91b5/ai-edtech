
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


        # st.write(f'grade is {grade}')



        units = db.get_unit_name(grade)

        ### 화면 구성

        st.header("학습메뉴")
        col1, padding, col2, col3, col4, col5 = st.columns([3,1,2,2,2,2])
        with col1:
            unit_id = st.selectbox(
                "단원을 선택해주세요",
                units,
                index = None,
                placeholder = "단원명",
                )

        if unit_id:
            # 원래는 학생 level 반영해서 문제 리스트 가져옴
            # problems = db.get_problems(unit_id, student_id)
            problems = db.get_problem_list()
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
        st.write("로그인이 필요합니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("home")
else:
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")