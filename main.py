import streamlit as st

st.set_page_config(page_title = "AI-EdTech")
st.subheader("신청 조회 및 취소")
with st.form("my_form1"):
    sid = st.text_input('Student ID:', autocomplete="on", placeholder="학번입력", max_chars=10)
    spwd = st.text_input('Password:', type='password', max_chars=4, help='4자리 비밀번호 입력')
    submitted = st.form_submit_button("조회")

from streamlit_option_menu import option_menu
import problemset, account

class MultiApp:
	def __init__(self):
		self.apps = [] 
	def add_app(self, title, function):
		self.apps.append({
			"title": title,
			"function": function
		})
	
	def run():
		with st.sidebar:
			app = option_menu(
			menu_title = 'Menu',
			options=['Main', 'Problem-sets', 'Account'],
			icons=['house-fill', 'trophy-fill', 'person-circle'],
			menu_icon='chat-text-fill',
			default_index=1,
			styles={
				"container": {"padding": "5!important", "background-color": 'black'},
				"icon": {"color": "white", "font-size": "23px"},
				"nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
				"nav-link-selected": {"background-color": "#02ab21"},}
				)
    # run the app function inside the main.py file
		if app == 'Problem-sets':
			problemset.app() 
		if app == 'Account':
			account.app() 
	
	run()
