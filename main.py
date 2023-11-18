import streamlit as st
	def app():
		with st.form("form1"):
	    		sid = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
				spwd = st.text_input('Password:', type='password', placeholder="4자리 비밀번호 입력", max_chars=4)
	    		submitted = st.form_submit_button("로그인")
		df = run_query('SELECT * FROM student ORDER BY sid ')
		st.table(df)
