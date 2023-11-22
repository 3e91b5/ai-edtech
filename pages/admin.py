import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import src.db as db

st.write('admin page')

if st.session_state['login'] == True:
    if st.session_state['admin'] == True:
        submitted = st.button('View all users')
        if submitted:
            st.write(db.view_all_users())
        
    
    else:
        st.write("Not authorized")
        switch_page("main") 
    
else:
    st.write("로그인이 필요합니다.")
    switch_page("main")



def delete_user(sid):
    result = db.delete_user(sid)
    if result:
        st.success("Deleted user")
    else:
        st.error("Failed to delete user")
