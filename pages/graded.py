
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


        if 'problem_id' not in st.session_state or st.session_state['problem_id'] == None:
            st.session_state['problem_id'] = 195
        student_id = st.session_state['student_id']
        # problem_id = st.session_state['problem_id']
        # st.session_state['name'] 들어가야 함. 현재는 임의의 값 넣은 상태.
        name = st.session_state['name']
        answer = db.get_selected_problem(st.session_state['problem_id'])

        problem_progress = db.get_problem_progress(student_id, st.session_state['problem_id'])

        selected = option_menu(None, ["채점결과", "학습메뉴", "챗봇과 얘기하기", "다음 문제로 이동"], # index 0 should be this page
            icons=['', 'house', 'chat', 'arrow-right-square'],
            menu_icon="cast", default_index=0, orientation="horizontal")

        st.subheader("문제 번호: "+str(st.session_state['problem_id']))
        problem = db.get_selected_problem(st.session_state['problem_id'])
        st.write(problem['question'][0])
        st.markdown("***")

        st.subheader(f"{st.session_state['name']}님의 답안")
        # ans_dct = ast.literal_eval(problem_progress['student_answer'][0])
        # for key, value in ans_dct.items():
        #     # /f가 whitespace로 인식되어 파이썬에서 자동 지워지기 때문에 정규식 수정해줘야 함
        #     value = re.sub(r'\f', r'\\f', value)
        #     st.write(key+": ")
        #     st.write(value)
        st.write(problem_progress['student_answer'][0])

        st.markdown("***")
        st.subheader("피드백")
        st.write(problem_progress['feedback'][0])
        st.markdown("***")
        st.subheader("채점 결과")
        # student_knowledge_score = problem_progress['knowledge_score'][0]
        # st.write(problem_progress['knowledge_score'])
        # st.write(student_knowledge_score)
        student_total_score = problem_progress['score'][0]
        # problem_knowledge_score = problem['knowledge_score'][0]
        student_knowledge_score = problem_progress['knowledge_score'][0]
        student_total_score = round(problem_progress['score'],2)[0]
        problem_knowledge_score = answer['knowledge_score'][0]
        st.markdown("총 점수: {0}점/10점".format(student_total_score))
        st.markdown("지식요소별 이해도")
        count = 0
        for key in problem_knowledge_score.keys():
            count +=1
            st.markdown(" - {0}: {1}점 / {2}점".format(key, student_knowledge_score[int(count)-1],problem_knowledge_score[key]))

        st.markdown("***")

        st.subheader("AI 해설")
        sol_dct = ast.literal_eval(answer["solution"][0])
        for key, value in sol_dct.items():
            # /f가 whitespace로 인식되어 파이썬에서 자동 지워지기 때문에 정규식 수정해줘야 함
            value = re.sub(r'\f', r'\\f', value)
            st.write(key+": ")
            st.write(value)

        if selected == "학습메뉴":
            switch_page('menu')
        if selected == "챗봇과 얘기하기":
            switch_page('Chat with ai2')
        if selected == "다음 문제로 이동":
            #st.session_state['problem_id'] = recommend_problem(unit_id, student_id, problem_id):
            st.session_state['problem_id'] = st.session_state['problem_id'] + 1
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
