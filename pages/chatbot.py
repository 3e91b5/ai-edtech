import streamlit as st
import src.gpt as gpt
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title = "Chatbot",
)
# gpt_client_teacher = None
try:
    st.write("Demo page for testing GPT")
    if st.session_state['login'] == True:
        st.write("chatbot page")   
        with st.form('authkey'):
            apikey = st.text_input('인증키를 입력하세요')
            submitted = st.form_submit_button("인증하기")
            if submitted:
                gpt.set_apikey(apikey)
                global gpt_client_teacher
                reponse , st.session_state['gpt_client'] = gpt.run_gpt_helloworld()
                st.write(reponse)
                st.session_state['gpt_session'] = True
                
            



        with st.form('chatbot'):
            question = st.text_input('질문을 입력하세요')
            submitted = st.form_submit_button("질문하기")
            
            if submitted:
                if st.session_state['gpt_session'] == True:
                    query = gpt.prompt(question)
                    response  = gpt.run_gpt(query, st.session_state['gpt_client'])
                    st.write(response)
                else:
                    st.write("인증키를 입력하세요")
            
                
except Exception as e:
    st.write(e)
    st.write("로그인이 필요합니다.")
    clicked = st.button('Go to main page')
    if clicked:
        switch_page("main")