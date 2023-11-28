from openai import OpenAI
import src.gpt as gpt
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config, add_page_title

# add_page_title()
# show_pages_from_config()

# Using session_state to store client and message history
# st.session_state['gpt_client'] : openai client
# st.session_state['gpt_session'] : boolean. True if client is initialized, False otherwise. maybe this can be used for retrieve chat history session from database
# st.session_state['messages'] : a list of message history. all messages are stored as a dictionary with two keys: role and content
# st.session_state['openai_model'] : openai model name. default is gpt-3.5-turbo



if 'login' in st.session_state:
    if st.session_state['login'] == True:
        st.title("ChatGPT-like clone")


        # init client
        with st.form('authkey_chatgpt'):
            apikey = st.text_input('인증키를 입력하세요')
            submitted = st.form_submit_button("인증하기")
            if submitted:
                gpt.set_apikey(apikey)
                
                reponse , st.session_state['gpt_client'] = gpt.run_gpt_helloworld()
                st.session_state.messages.append({"role": "assistant", "content": reponse})
                # st.write(reponse)
                
                # st.session_state initialized
                st.session_state['gpt_session'] = True
                st.session_state['openai_model'] = "gpt-3.5-turbo"
                st.session_state['messages'] =  gpt.default_prompt()
        
        # clear chat_message session button
        clear_message = st.button("Clear chat history")
        if clear_message:
            st.session_state.messages = []
            
        # client = OpenAI(api_key=apikey)
        client = st.session_state['gpt_client']

        # Set a default model
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = gpt.default_prompt()

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
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
    
    else: # not logged in
        # st.session_state['login'] == False
        st.write("로그인이 필요합니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("home")
            
else: # unintended access
    # 'login' not in st.session_state
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")
