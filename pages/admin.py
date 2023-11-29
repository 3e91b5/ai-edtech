import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import src.db as db
from st_pages import show_pages_from_config, add_page_title
# add_page_title()
# show_pages_from_config()


st.set_page_config(
    page_title = "Admin",
)


st.write('admin page')
try:
    if st.session_state['login'] == True:
        if st.session_state['admin'] == True: # Admin page
            
            # delete user menu
            with st.form("delete_user"):
                account = st.text_input('Delete ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
                submitted = st.form_submit_button("Delete user")
                if submitted:
                    success = db.delete_user(account)
                    if success: 
                        st.success(f"User '{account}' deleted")
                    else:
                        st.error("User not found")
                        
            # view all users menu
            submitted = st.button('View all users')
            if submitted:
                st.write(db.view_all_users())
            
        
        else: # not admin
            st.write("Not authorized")
            clicked = st.button('Go to main page')
            if clicked:
                switch_page("home")
            
        
    else: # not logged in
        st.write("로그인이 필요합니다.")
        clicked = st.button('Go to main page')
        if clicked:
            switch_page('home')
        
    # switch_page("home")

        # switch_page("home")
except Exception as e:
    switch_page("home")


    