import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import src.db as db
import src.gpt as gpt
import pandas as pd
import io
import base64
from PIL import Image

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

import os

# 파일 업로드 함수
def save_uploaded_file(directory, file):
    if not os.path.exists(directory): 
        os.makedirs(directory)
        
    with open(os.path.join(directory, file.name) ,'wb') as f: 
        f.write(file.getbuffer()) 
    
    if os.path.exists(os.path.join(directory, file.name)):
        st.success('파일 업로드 성공')
        return True
    else:
        st.error('파일 업로드 실패')
        return False

### 화면 구성
if 'login' in st.session_state:
    if st.session_state['login'] == True:
        if st.session_state['problem_id'] == None:
            switch_page('menu')
            
        problem_id = st.session_state['problem_id']
        student_id = st.session_state['student_id']
        problem = db.get_selected_problem(problem_id)

        selected = None
        selected = option_menu(None, ["문제풀기", "학습메뉴", "모르겠어요", "제출하기"], # index 0 should be this page
            icons=['book','house', 'emoji-frown', 'cloud-upload'],
            menu_icon="cast", default_index=0, orientation="horizontal")

        st.subheader("문제 번호: "+ str(problem_id))
        st.write(problem['question'][0])
        st.markdown("***")
        st.subheader("답안을 작성해주세요")

        uploaded_file = st.file_uploader("Upload your answer image file (e.g. png, jpg, jpeg)")
        if uploaded_file is not None:
            # # file save name format: {student_id}_{problem_id}.{file_extension}
            # uploaded_file.name = str(st.session_state['student_id']) +'_'+str(st.session_state['problem_id'])+  '.' + uploaded_file.name.split('.')[-1]
            # uploaded_file_url = 'content/'+ uploaded_file.name
            # answer_uploaded = save_uploaded_file('content', uploaded_file) # save answer of student in local server TODO: need to change to save in DB
            
            # if answer_uploaded:
            #     st.success('답안 제출 성공')
            # else:
            #     st.error('답안 제출 실패')
            st.image(uploaded_file, use_column_width=True)
            # base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
            # image_bytes = base64.b64decode(base64_image)
            # st.image(image_bytes, use_column_width=True)

        if selected == "학습메뉴":
            switch_page('menu')
        if selected == "모르겠어요":
            st.toast(problem['hint'][0])
            
        if selected == "제출하기":
            if uploaded_file is not None:
                gpt.grade_answer(student_id, problem_id,uploaded_file)
                switch_page('graded Result')
            else:
                st.toast("답안을 제출해주세요.")
    else:
        st.write("로그인이 필요합니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("home")
else:
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")
