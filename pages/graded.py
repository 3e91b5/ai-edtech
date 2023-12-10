import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import src.db as db
import json
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
        problem = db.get_selected_problem(problem_id)
        st.write(problem['question'][0])
        st.markdown("***")

        st.subheader("AI 해설")

        test = answer["solution"][0]
        unescaped_string = re.sub(r'\frac', r'\frac', test)
        sol_dct = ast.literal_eval(unescaped_string)
        for key, value in sol_dct.items():
            st.write(key+": ")
            st.write(value)
        st.markdown("***")

        st.subheader(f"{st.session_state['name']}님의 답안")
        st.write(solved_answer['student_answer'][0])

        st.markdown("***")

        st.subheader("채점 결과")
        step_criteria_json = answer['step_criteria'][0]
        print(step_criteria_json)
        # step_criteria = json.loads(answer['step_criteria'])
        # print('answer', answer)
        # print('solved_answer', solved_answer)
        count = 0
        for k in step_criteria_json:
            count +=1
            st.markdown("{0}: {1}점 / {2}점".format(step_criteria_json[k], answer['step_score'][0][int(count)-1], solved_answer['step_score'][0][int(count)-1]))

        # for i in range(len(step_criteria)):
        #     st.markdown("{0}: {1}점 / {2}점".format(step_criteria.values()[i], answer['step_score'][i], solved_answer['score'][i]))

        # st.subheader(":red[최종 점수: {0}점]".format(answer['total_score']))
        st.subheader(":red[최종 점수: {0}점]".format(solved_answer['total_score'][0]))

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
