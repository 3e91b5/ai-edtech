import streamlit as st

# def app():
st.write("account page")

if st.session_state['login']== True:
  if st.session_state['teacher'] == True:
    # account menu for teacher
    pass
  else: 
    # account menu for student
    pass