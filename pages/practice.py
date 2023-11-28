import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import src.db as db
import src.gpt as gpt
from st_pages import show_pages_from_config, add_page_title
from io import StringIO

# add_page_title()
# show_pages_from_config()

# 수식 left align 설정
st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)
if 'login' in st.session_state:
    if st.session_state['login'] == True:
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
        selected = None
        selected = option_menu(None, ["문제풀기", "학습메뉴", "모르겠어요", "제출하기"], # index 0 should be this page
            icons=['book','house', 'emoji-frown', 'cloud-upload'],
            menu_icon="cast", default_index=0, orientation="horizontal")

        st.subheader("문제 번호: "+ str(problem_id))
        # problem['question'] 들어감. 아래는 임의로 입력한 값.
        st.latex(r'''
            \text{공정한 6면 주사위를 5번 던집니다. 2번 이하로 6이 나올 확률은 얼마인가요?}
        ''')

        # answer['solution'] 들어감. 아래는 임의로 입력한 값.
        st.subheader("정답 풀이")
        st.latex(r'''
        \text{정확히 2번 6이 나올 방법의 수는 }\binom{5}{2}5^3 \text{입니다.}  \\
        \text{6이 나올 두 주사위를 고르는 방법이 }\binom{5}{2}\text{가지이고, 나머지 3개 주사위에 대해서는 각각 5가지 선택이 가능합니다.}  \\
        \text{마찬가지로, 정확히 1번 6이 나올 방법의 수는 }\binom{5}{1}5^4\text{이며, 6이 한 번도 나오지 않는 방법의 수는 }\binom{5}{0}5^5\text{입니다.}  \\
        \text{따라서 확률은 }\frac{\binom{5}{2}5^3+\binom{5}{1}5^4+\binom{5}{0}5^5}{6^5}=\frac{625}{648}\text{입니다.}
        ''')

        # solved_answer['solved'] 들어감. 아래는 임의로 입력한 값.
        st.subheader(f"{st.session_state['name']}님의 답안")
        st.latex(r'''
        \text{6이 2번 나오는 경우의 수 = }\binom{5}{2}5^3  \\
        \text{2개 주사위에서 6 나오려면}\binom{5}{2}\text{경우의 수 and 3개 주사위에서 1 부터 5 나온다}  \\
        \text{6이 1번 나오는 경우의 수 = }\binom{5}{1}5^4\text{, 0번 나오는 경우의 수 = }\binom{5}{0}5^5  \\
        \text{따라서 }\frac{\binom{5}{2}5^3+\binom{5}{1}5^4+\binom{5}{0}5^5}{6^5}=\frac{625}{648}
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
            st.toast("이 문제는 "+problem['hint']+" 개념을 활용해 풀 수 있어요!")
        if selected == "제출하기":
            '''
            streamlit은 tabletPC 화면 상의 input 처리하는 기능이 없음 + ocr은 image url로 넣음.
            solved = "https://market.edugorilla.com/wp-content/uploads/sites/5/2017/07/algebra-hand.png"
            ocr_solved = gpt.get_ocr(solved)
            gpt.scored(ocr_solved)
            '''
            switch_page('graded')
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