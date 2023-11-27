import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import src.db as db
import src.gpt as gpt
from st_pages import show_pages_from_config, add_page_title
add_page_title()
show_pages_from_config()

# 수식 left align 설정
st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

# 힌트 메세지(toast) 디자인 변경
st.markdown(
        """
        <style>
            div[data-testid=stToast] {
                padding:  20px 10px 40px 10px;
                margin: 10px 400px 200px 10px;
                background-color: #454545;
                width: 30%;
            }

            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                font-size: 15px; font-style: normal; font-weight: 400;
                foreground-color: #FFFFFF;
            }
        </style>
        """, unsafe_allow_html=True
)

### 변수 가져오기
problem_id = 1 # st.session_state['problem_id']
problem = db.get_selected_problem(problem_id)

### 화면 구성
selected = option_menu(None, ["학습메뉴", "모르겠어요", "제출하기"],
    icons=['house', 'emoji-frown', 'cloud-upload'],
    menu_icon="cast", default_index=0, orientation="horizontal")

st.subheader("문제 번호: "+"problem_id")
st.latex(r'''
    problem['question']
''')

st.markdown("***")
st.subheader("답안을 작성해주세요")
st.image(Image.open('answer_sample.png'))

if selected == "학습메뉴":
    switch_page('menu')
if selected == "모르겠어요":
    st.toast("이 문제는 "+problem['hint']+" 개념을 활용해 풀 수 있어요!")
if selected == "제출하기":
    '''
    streamlit은 tabletPC 화면 상의 input 처리하는 기능이 없음 + ocr은 image url로 넣음.
    solved = "https://market.edugorilla.com/wp-content/uploads/sites/5/2017/07/algebra-hand.png"
    ocr_solved = gpt.get_ocr(solved)
    gpt.scored(ocr_solved)
    '''
    switch_page('graded')