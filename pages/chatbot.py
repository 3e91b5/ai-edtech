import streamlit as st
import src.gpt as gpt
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, add_page_title
import random
import time
import openai as OpenAI
# add_page_title()
# show_pages_from_config()


def get_apikey():
    return st.session_state["api_key"]



st.set_page_config(
    page_title = "Chatbot",
)
# gpt_client_teacher = None
if 'login' in st.session_state:
    if st.session_state['login'] == True:
        st.write("Demo page for testing GPT")
        if st.session_state['login'] == True:
            st.write("chatbot page")   
            with st.form('authkey'):
                apikey = st.text_input('인증키를 입력하세요')
                submitted = st.form_submit_button("인증하기")
                if submitted:
                    gpt.set_apikey(apikey)
                    
                    reponse , st.session_state['gpt_client'] = gpt.run_gpt_helloworld()
                    st.write(reponse)
                    st.session_state['gpt_session'] = True
                    
                


            #basic question
            
            with st.form('basic_question'):
                question = st.text_input('질문을 입력하세요')
                submitted = st.form_submit_button("질문하기")
                
                if submitted:
                    if st.session_state['gpt_session'] == True:
                        query = gpt.default_prompt(question)
                        response  = gpt.run_gpt(query, st.session_state['gpt_client'])
                        st.write(response)
                    else:
                        st.write("인증키를 입력하세요")
            
            # prompt example
            prompt = st.chat_input("질문을 입력하세요")
            if prompt:
                st.write(f"User has sent the following prompt: {prompt}")
            
            
            

            

            
            
            
            # interactive chatbot example
            st.title("Simple Chat")
            
            # clear chat_message session
            clear_message = st.button("Clear chat history")
            if clear_message:
                st.session_state.messages = []
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Accept user input
            if prompt := st.chat_input("What is up?"):
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
            
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = random.choice(
                    [
                        "Hello there! How can I assist you today?",
                        "Hi, human! Is there anything I can help you with?",
                        "Do you need help?",
                    ]
                )
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            
            
            # # chatGPT-like clone example
            # st.title("ChatGPT-like clone example")


            # client = OpenAI(
            #     # api_key=st.secrets["OPENAI_API_KEY"]
            #     api_key=get_apikey(),
            #     )

            # if "openai_model" not in st.session_state:
            #     st.session_state["openai_model"] = "gpt-3.5-turbo"

            # if "messages" not in st.session_state:
            #     st.session_state.messages = []

            # for message in st.session_state.messages:
            #     with st.chat_message(message["role"]):
            #         st.markdown(message["content"])

            # if prompt := st.chat_input("What is up?"):
            #     st.session_state.messages.append({"role": "user", "content": prompt})
            #     with st.chat_message("user"):
            #         st.markdown(prompt)

            #     with st.chat_message("assistant"):
            #         message_placeholder = st.empty()
            #         full_response = ""
            #         for response in client.chat.completions.create(
            #             model=st.session_state["openai_model"],
            #             messages=[
            #                 {"role": m["role"], "content": m["content"]}
            #                 for m in st.session_state.messages
            #             ],
            #             stream=True,
            #         ):
            #             full_response += (response.choices[0].delta.content or "")
            #             message_placeholder.markdown(full_response + "▌")
            #         message_placeholder.markdown(full_response)
            #     st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.write("로그인이 필요한 서비스입니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("main")        
else:
    st.write("로그인이 필요한 서비스입니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("main")