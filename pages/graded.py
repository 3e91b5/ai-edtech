
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import src.db as db
import json
import ast
import re
import ast
import re
### 디자인 변경
# 수식 left align
st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

# indentation 변경
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True
)

### 화면 구성
if 'login' in st.session_state:
    if st.session_state['login'] == True:
        # st.session_state['problem_id'] 들어가야 함. 현재는 임의의 값 넣은 상태.
        problem_id = st.session_state['problem_id']
        student_id = st.session_state['student_id']
        # st.session_state['name'] 들어가야 함. 현재는 임의의 값 넣은 상태.
        # name = 홍길동
        name = st.session_state['name']
        
        answer = db.get_selected_problem(problem_id)
        solved_answer = db.get_answer(problem_id, student_id)

        selected = option_menu(None, ["채점결과", "학습메뉴", "챗봇과 얘기하기", "다음 문제로 이동"], # index 0 should be this page
            icons=['', 'house', 'chat', 'arrow-right-square'],
            menu_icon="cast", default_index=0, orientation="horizontal")

        st.subheader("문제 번호: "+str(problem_id))
        #qst = ast.literal_eval(answer["question"][0])
        st.write(answer["question"][0])
        st.markdown("***")

        st.subheader("AI 해설")
        sol_dct = ast.literal_eval(answer["solution"][0])
        for key, value in sol_dct.items():
            # /f가 whitespace로 인식되어 파이썬에서 자동 지워지기 때문에 정규식 수정해줘야 함
            value = re.sub(r'\f', r'\\f', value)
            st.write(key+": ")
            st.write(value)
        st.markdown("***")

        st.subheader(f"{st.session_state['name']}님의 답안")
        ans_dct = ast.literal_eval(solved_answer['student_answer'][0])
        for key, value in ans_dct.items():
            # /f가 whitespace로 인식되어 파이썬에서 자동 지워지기 때문에 정규식 수정해줘야 함
            value = re.sub(r'\f', r'\\f', value)
            st.write(key+": ")
            st.write(value)

        st.markdown("***")
        st.subheader("피드백")
        feedback = solved_answer['feedback'][0]
        st.write(feedback)
        st.markdown("***")

        student_knowledge_score = solved_answer['knowledge_score'][0]
        student_total_score = round(solved_answer['score'],2)[0]
        problem_knowledge_score = answer['knowledge_score'][0]
        st.subheader("채점 결과") 
        st.markdown("총 점수: {0}점".format(student_total_score))
        st.markdown("지식요소별 이해도")
        count = 0
        for key in problem_knowledge_score.keys():
            count +=1
            st.markdown(" - {0}: {1}점 / {2}점".format(key, problem_knowledge_score[key], student_knowledge_score[int(count)-1]))

        if selected == "학습메뉴":
            switch_page('menu')
        if selected == "챗봇과 얘기하기":
            switch_page('chat with ai')
        if selected == "다음 문제로 이동":
            #st.session_state['problem_id'] = recommend_problem(unit_id, student_id, problem_id):
            st.session_state['problem_id'] = 2
            switch_page('question')
    else:
        st.write("로그인이 필요한 서비스입니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("home")
else:
    st.write("로그인이 필요한 서비스입니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")
