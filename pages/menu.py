import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import src.db as db
import src.app as app 
from st_pages import show_pages_from_config, add_page_title
# add_page_title()
# show_pages_from_config()

if 'login' in st.session_state:
    if st.session_state['login'] == True:
        ### 변수 가져오기
        student_id = st.session_state['student_id']
        grade = db.get_student_grade(student_id)
        st.write(f'grade is {grade}')
        units = db.get_units(grade)


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
            problems = db.get_problems()
            problems['solved'] = db.get_history(problems, student_id)
            
            for item in range(len(problems['problem_id'])):
                if item < 5:
                    with col2:
                        app.question_buttons(problems, item)
                elif (item >= 5 and item < 10):
                    with col3:
                        app.question_buttons(problems, item)
                elif (item >= 10 and item < 15):
                    with col4:
                        app.question_buttons(problems, item)
                else:
                    with col5:
                        app.question_buttons(problems, item)
        
        from PIL import Image
        image1 = Image.open('pages/menu1.jpg')
        st.image(image1, use_column_width=True, caption='demo1')
        
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
