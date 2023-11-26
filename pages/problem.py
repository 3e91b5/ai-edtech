import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import src.db as db
import src.gpt as gpt
# db에서 문제 가져옴. 아래는 임의로 값 입력한 상태.
'''
qid = st.session_state['qid']
problem = db.get_selected_problem(qid)
'''
qid = "Q101"
hint = "좌극한, 우극한"

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

### 화면 구성
selected = option_menu(None, ["학습메뉴", "모르겠어요", "제출하기"],
    icons=['house', 'emoji-frown', 'cloud-upload'],
    menu_icon="cast", default_index=0, orientation="horizontal")

st.subheader("문제 번호: "+qid)
# db에서 가져온 문제 입력. 아래는 임의로 입력한 값.
st.latex(r'''
    \text{공정한 6면 주사위를 5번 던집니다. 2번 이하로 6이 나올 확률은 얼마인가요?}
''')

st.markdown("***")
st.subheader("답안을 작성해주세요")
st.image(Image.open('answer_sample.png'))

if selected == "학습메뉴":
    switch_page("menu")
if selected == "모르겠어요":
    st.toast("이 문제는 "+hint+" 개념을 활용해 풀 수 있어요!")
if selected == "제출하기":
    # streamlit은 tabletPC 화면 상의 input 처리하는 기능이 없음. 이번 demo에선 학생 답안을 image url로 넣음.
    solved = "https://market.edugorilla.com/wp-content/uploads/sites/5/2017/07/algebra-hand.png"
    ocr_solved = gpt.get_ocr(solved)
    #score = gpt.scored(ocr_solved)
    #db.update_solved(qid, sid, score, ocr_solved)
    switch_page("solved")