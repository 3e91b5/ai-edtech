
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
#        st.latex(r'''
#            \text{모든 양의 정수 } n \text{에 대하여, } f(n) = \log_{2002} n^2 \text{라고 할 때, } f(11) + f(13) + f(14) \text{의 값을 구하시오.}
#        ''')
        st.write('모든 양의 정수 $n$에 대하여, $f(n)=\\log_{2002} n^2$라고 할 때, $f(11)+f(13)+f(14)$의 값을 구하시오.')
        st.markdown("***")
        # answer['solution'] 들어가야 함. 아래는 임의로 입력한 값.
        st.subheader("해설 (step-by-step solution으로 gpt 통해 다시 뽑은 상태에요)")
        st.latex(r'''
            \begin{align*}
            1. & \quad \text{주어진 함수는 다음과 같습니다: } f(n) = \log_{2002} n^2 \\
            2. & \quad \text{함수를 로그의 성질을 이용하여 재표현합니다: } f(n) = 2 \cdot \log_{2002} n \\
            3. & \quad \text{값 대입하여 식을 구성합니다: } 2 \cdot \log_{2002} 11 + 2 \cdot \log_{2002} 13 + 2 \cdot \log_{2002} 14 \\
            4. & \quad \text{로그의 밑 변환을 통해 편리한 로그 형태로 변환합니다: } 2 \cdot \log_{10} 11 + 2 \cdot \log_{10} 13 + 2 \cdot \log_{10} 14 \\
            5. & \quad \text{로그 합병을 통해 식을 간소화합니다: } \log_{10} (11^2 \cdot 13^2 \cdot 14^2) \\
            6. & \quad \text{최종 답: } \log_{10} (11^2 \cdot 13^2 \cdot 14^2)
            \end{align*}
        ''')
        st.markdown("***")
        # solved_answer['solved'] 들어가야 함. 아래는 임의로 입력한 값.
        st.subheader(f"{st.session_state['name']}님의 답안")
        st.latex(r'''
            \begin{align*}
            & f(n) = \log_{2002} n^2 = 2 \cdot \log_{2002} n. \\
            & \text{다시 쓰면 }2 \cdot \log_{2002} 11 + 2 \cdot \log_{2002} 13 + 2 \cdot \log_{2002} 14. \\
            & \text{정리하면 } 2 \cdot \log_{10} 11 + \log_{10} 13 + \log_{10} 14. \\
            & \text{그러므로 정답은 } \log_{10} (11 \cdot 13 \cdot 14).
            \end{align*}
        ''')
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
        st.subheader("채점 결과 (홍식님 prompt의 step_score 내용)")
        step_criteria_json = answer['step_criteria'][0]
        print(step_criteria_json)
        # step_criteria = json.loads(answer['step_criteria'])
        # print('answer', answer)
        # print('solved_answer', solved_answer)
        count = 0
        for k in step_criteria_json:
            count +=1
            st.markdown("{0}: {1}점 / {2}점".format(step_criteria_json[k], answer['step_score'][0][int(count)-1], solved_answer['step_score'][0][int(count)-1]))
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
