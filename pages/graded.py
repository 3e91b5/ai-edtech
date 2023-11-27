import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import src.db as db

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
 
# 임의의 값 사용
problem_id = "Q101"
student_id = "A100"
name = "홍길동"
answer = db.get_solution(problem_id)
solved_answer = db.get_solved(problem_id, student_id)
'''
student_id = st.session_state['student_id']
name = st.session_state['name']
'''
### 화면 구성
selected = option_menu(None, ["학습메뉴", "챗봇과 얘기하기", "다음 문제로 이동"],
    icons=['house', 'chat', 'arrow-right-square'],
    menu_icon="cast", default_index=0, orientation="horizontal")

st.subheader("문제 번호: "+problem_id)
# db에서 가져온 문제 입력. 아래는 임의로 입력한 값.
st.latex(r'''
    \text{공정한 6면 주사위를 5번 던집니다. 2번 이하로 6이 나올 확률은 얼마인가요?}
''')
st.markdown("***")

# answer['solution'] 들어감. 아래는 임의로 입력한 값.
st.subheader("정답 풀이")
st.latex(r'''
\text{정확히 2번 6이 나올 방법의 수는 }\binom{5}{2}5^3 \text{입니다.}  \\
\text{6이 나올 두 주사위를 고르는 방법이 }\binom{5}{2}\text{가지이고, 나머지 3개 주사위에 대해서는 각각 5가지 선택이 가능합니다.}  \\
\text{마찬가지로, 정확히 1번 6이 나올 방법의 수는 }\binom{5}{1}5^4\text{이며, 6이 한 번도 나오지 않는 방법의 수는 }\binom{5}{0}5^5\text{입니다.}  \\
\text{따라서 확률은 }\frac{\binom{5}{2}5^3+\binom{5}{1}5^4+\binom{5}{0}5^5}{6^5}=\frac{625}{648}\text{입니다.}
''')
st.markdown("***")

# solved_answer['solved'] 들어감. 아래는 임의로 입력한 값.
st.subheader(f"{name}님의 답안") 
st.latex(r'''
\text{6이 2번 나오는 경우의 수 = }\binom{5}{2}5^3  \\
\text{2개 주사위에서 6 나오려면}\binom{5}{2}\text{경우의 수 and 3개 주사위에서 1 부터 5 나온다}  \\
\text{6이 1번 나오는 경우의 수 = }\binom{5}{1}5^4\text{, 0번 나오는 경우의 수 = }\binom{5}{0}5^5  \\
\text{따라서 }\frac{\binom{5}{2}5^3+\binom{5}{1}5^4+\binom{5}{0}5^5}{6^5}=\frac{625}{648}
''')
st.markdown("***")
st.subheader("채점 결과")
for i in range(len(answer['step_criteria'])):
    st.markdown("{0}: {1}점 / {2}점".format(list(answer['step_criteria'])[i], answer['step_score'][i], solved_answer['score'][i]))

st.subheader(":red[최종 점수: {0}점]".format(answer['total_score']))

if selected == "학습메뉴":
    switch_page("menu")
if selected == "챗봇과 얘기하기":
    switch_page("chatbot")
if selected == "다음 문제로 이동":
    #st.session_state['problem_id'] = recommend_problem(unit_id, student_id, problem_id):
    switch_page("problem")