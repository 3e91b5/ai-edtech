
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import src.db as db
import json

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
        problem_id = 1 
        student_id = st.session_state['student_id']
        # st.session_state['name'] 들어가야 함. 현재는 임의의 값 넣은 상태.
        name = '홍길동' 
        answer = db.get_solution(problem_id)
        solved_answer = db.get_answer(problem_id, student_id)

        selected = option_menu(None, ["채점결과", "학습메뉴", "챗봇과 얘기하기", "다음 문제로 이동"], # index 0 should be this page
            icons=['', 'house', 'chat', 'arrow-right-square'],
            menu_icon="cast", default_index=0, orientation="horizontal")

        st.subheader("문제 번호: "+str(problem_id))
        # problem['question'] 들어가야 함. 아래는 임의로 입력한 값.
        st.latex(r'''
            \text{공정한 6면 주사위를 5번 던집니다. 2번 이하로 6이 나올 확률은 얼마인가요?}
        ''')
        st.markdown("***")
        # answer['solution'] 들어가야 함. 아래는 임의로 입력한 값.
        st.subheader("정답 풀이")
        st.latex(r'''
        \text{정확히 2번 6이 나올 방법의 수는 }\binom{5}{2}5^3 \text{입니다.}  \\
        \text{6이 나올 두 주사위를 고르는 방법이 }\binom{5}{2}\text{가지이고, 나머지 3개 주사위에 대해서는 각각 5가지 선택이 가능합니다.}  \\
        \text{마찬가지로, 정확히 1번 6이 나올 방법의 수는 }\binom{5}{1}5^4\text{이며, 6이 한 번도 나오지 않는 방법의 수는 }\binom{5}{0}5^5\text{입니다.}  \\
        \text{따라서 확률은 }\frac{\binom{5}{2}5^3+\binom{5}{1}5^4+\binom{5}{0}5^5}{6^5}=\frac{625}{648}\text{입니다.}
        ''')
        st.markdown("***")
        # solved_answer['solved'] 들어가야 함. 아래는 임의로 입력한 값.
        st.subheader(f"{st.session_state['name']}님의 답안")
        st.latex(r'''
        \text{6이 2번 나오는 경우의 수 = }\binom{5}{2}5^3  \\
        \text{2개 주사위에서 6 나오려면}\binom{5}{2}\text{경우의 수 and 3개 주사위에서 1 부터 5 나온다}  \\
        \text{6이 1번 나오는 경우의 수 = }\binom{5}{1}5^4\text{, 0번 나오는 경우의 수 = }\binom{5}{0}5^5  \\
        \text{따라서 }\frac{\binom{5}{2}5^3+\binom{5}{1}5^4+\binom{5}{0}5^5}{6^5}=\frac{625}{648}
        ''')
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
