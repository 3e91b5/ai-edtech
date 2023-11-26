import streamlit as st
import src.gpt as gpt


st.write("Demo page for testing GPT")
if st.session_state['login'] == True:
    st.write("chatbot page")   
    with st.form('authkey'):
        apikey = st.text_input('인증키를 입력하세요')
        submitted = st.form_submit_button("인증하기")
        if submitted:
            gpt.set_apikey(apikey)
            gpt.run_gpt_helloworld()
            
        



    with st.form('chatbot'):
        question = st.text_input('질문을 입력하세요')
        submitted = st.form_submit_button("질문하기")
        if submitted:
            query = gpt.prompt(question)
            result  = gpt.run_gpt(query)
            st.write(result)
    