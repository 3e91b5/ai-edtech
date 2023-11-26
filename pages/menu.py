import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import src.db as db
import src.app as app 

### toy data로 작업
problems = pd.read_excel('qid.xlsx')
topics = ['다항식','방정식과 부등식','경우의 수','행렬','도형의 방정식','집합과 명제','함수와 그래프']
'''
sid = st.session_state['sid']
grade = get_student_grade(sid)
topics = db.get_topics(grade)
'''
### 화면 구성
st.header("학습메뉴")
col1, padding, col2, col3, col4, col5 = st.columns([3,1,2,2,2,2])
with col1:
    tid = st.selectbox(
        "단원을 선택해주세요",
        topics,
        index = None,
        placeholder = "단원명",
        )

if tid:
    # 문제 리스트 db에서 가져오기. 지금은 임의로 입력한 값 사용.
    # problems = db.get_problems(tid, sid)
    for item in range(len(problems['qid'])):
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
