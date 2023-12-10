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
        problem = db.get_selected_problem(problem_id)
        st.write(problem['question'][0])
        problem = db.get_selected_problem(problem_id)
        st.write(problem['question'][0])
        st.markdown("***")

        st.subheader("AI 해설")
        #unescaped_string = re.sub(r'\f', r'\\f', test)
        #st.write(unescaped_string)
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
        st.write('''
            총점은 5점입니다. 미적분을 사용하여 최솟값을 찾는 과정을 올바르게 시작했지만, 솔루션에 중대한 오류가 있습니다.

            1. **임계점:**
            - 도함수를 올바르게 찾았지만 부호 오류가 있습니다. 올바른 방정식은 \( f'(n) = \frac{1}{2} - \frac{18}{n^2} = 0 \)입니다.

            2. **\(n\)에 대한 해:**
            - \(n^2 = 36\)을 올바르게 풀었지만, 우리는 양의 정수와 관련이 있으므로 유효한 해는 \(n = 6\)이며, \(n = -6\)이 아닙니다.

            3. **함수 평가:**
            - 최솟값이 \(n = -6\)에서 발생한다고 잘못 기술했습니다. 이는 문제에 대한 유효한 해가 아닙니다. \(n\)은 양의 정수여야 합니다.

            이러한 단계를 검토하고 필요한 수정을 가해주십시오.
        ''')
        st.markdown("***")

        st.subheader("채점 결과")
        student_knowledge_score = solved_answer['knowledge_score'][0]
        st.write(solved_answer['knowledge_score'])
        st.write(student_knowledge_score)
        student_total_score = solved_answer['score'][0]
        problem_knowledge_score = problem['knowledge_score'][0]

        count = 0
        #for k in problem_knowledge_score:
        #    count +=1
        #    st.markdown("{0}: {1}점 / {2}점".format(problem_knowledge_score[k], problem_knowledge_score[int(count)-1], student_total_score[int(count)-1]))

        for key in problem_knowledge_score.keys():
            count +=1
            st.write(key)
            st.write(problem_knowledge_score[key])
            st.write(student_total_score[int(count)-1])
            #st.markdown("{0}: {1}점 / {2}점".format(key, problem_knowledge_score[key], student_total_score.values()[int(count)-1]))

        st.markdown("***")
        # st.subheader(":red[최종 점수: {0}점]".format(solved_answer['total_score'][0]))
        st.subheader("지식요소별 이해도 (제가 새로 추가한 내용)")
        st.markdown("로그의 밑의 변환 공식: 1점 / 1점")
        st.markdown("로그의 여러 가지 공식: 2점 / 3점")
        st.markdown("로그의 밑과 진수의 조건: 0.5점 / 1점")

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
