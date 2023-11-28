
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import src.db as db
import src.gpt as gpt
from io import StringIO

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
# 힌트 메세지 디자인 변경

st.markdown(
    """
    <style>
        div[data-testid=stToast] {
            padding:  20px 10px 40px 10px;
            margin: 10px 400px 200px 10px;
            background-color: #ffffff;
            width: 30%;
         }
             
        [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
            font-size: 20px; font-style: normal; font-weight: 400;
        }
     </style>
     """, unsafe_allow_html=True
)

### 화면 구성
if 'login' in st.session_state:
    if st.session_state['login'] == True:

        # st.session_state['problem_id'] 들어가야 함. 현재는 임의의 값 넣은 상태.
        problem_id = 1 
        problem = db.get_selected_problem(problem_id)

        selected = None
        selected = option_menu(None, ["문제풀기", "학습메뉴", "모르겠어요", "제출하기"], # index 0 should be this page
            icons=['book','house', 'emoji-frown', 'cloud-upload'],
            menu_icon="cast", default_index=0, orientation="horizontal")

        st.subheader("문제 번호: "+ str(problem_id))
        # problem['question'] 들어감. 아래는 임의로 입력한 값.
        st.latex(r'''
            \text{공정한 6면 주사위를 5번 던집니다. 2번 이하로 6이 나올 확률은 얼마인가요?}
        ''')
        st.markdown("***")
        st.subheader("답안을 작성해주세요")

        uploaded_file = st.file_uploader("Upload your answer image file (e.g. png, jpg, jpeg)")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            st.write(bytes_data)

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.write(stringio)

            # To read file as string:
            string_data = stringio.read()
            st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)


        # st.image(Image.open('answer_sample.png'))

        if selected == "학습메뉴":
            switch_page('menu')
        if selected == "모르겠어요":
        # problem['hint'] 넣어야 함. 지금은 임의의 값
            st.toast('이 문제는 '+':red[힌트]'+' 개념을 활용해 풀 수 있어요!')
        if selected == "제출하기":
#            switch_page('graded')
            switch_page('Graded Result')
    else:
        st.write("로그인이 필요합니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("main")
else:
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("main")
