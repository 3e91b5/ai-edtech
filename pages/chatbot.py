import streamlit as st
import src.gpt as gpt
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, add_page_title
import random
import time
import openai as OpenAI
# add_page_title()
# show_pages_from_config()

st.set_page_config(
    page_title = "Chatbot",
)

def get_apikey():
    return st.session_state["api_key"]


def interactive_chatbot():
    # interactive chatbot
    st.title("Interactive Chatbot")
    
    with st.form('authkey_chatgpt'):
        apikey = st.text_input('인증키를 입력하세요')
        submitted = st.form_submit_button("인증하기")
        if submitted:
            
            # api call code for debugging
            if apikey == "":
                apikey = st.secrets["apikey"]
            gpt.set_apikey(apikey)
            
            response , st.session_state['gpt_client'] = gpt.run_gpt_helloworld()
            st.session_state.messages.append({"role": "assistant", "content": response})
            # # st.write(response)
            
            # st.session_state initialized
            st.session_state['gpt_session'] = True
            st.session_state['openai_model'] = "gpt-3.5-turbo"
            st.session_state['messages'] =  gpt.default_prompt()
            
    # clear chat_message session button
    clear_message = st.button("Clear chat history")
    if clear_message:
        st.session_state.messages = []
        
    if st.session_state['gpt_session'] == True: # authentication needed
        # client = OpenAI(api_key=apikey)
        client = st.session_state['gpt_client']

        # Set a default model
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = gpt.default_prompt()

        # Display chat messages from history on app rerun
        # TODO: 어떻게 해야 똑똑하게 첫번째 assistant prompt를 가릴 수 있지
        for message in st.session_state.messages:
            # st.write(message)
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # accept user input
        if prompt := st.chat_input("Ask math questions"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # st.write('model is ', st.session_state["openai_model"])
            # st.write(st.session_state.messages)
            
            # TODO: Don't print default prompt
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        


if 'login' in st.session_state:
    if st.session_state['login'] == True:
        interactive_chatbot()
        
            
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

