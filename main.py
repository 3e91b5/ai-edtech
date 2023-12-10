import streamlit as st
# from streamlit_option_menu import option_menu
import time
from streamlit_extras.switch_page_button import switch_page 
import datetime
# import pandas as pd
import src.db as db
from st_pages import Page, Section, show_pages
import base64

st.set_page_config(
    page_title = "AI-EdTech",
    initial_sidebar_state = "auto",  
)

show_pages(
    [
        Page("main.py", "Home", ':classical_building:'),
        Section(name="My Page", icon=':information_desk_person:'),
        Page("pages/info.py", "My Info"),
        Page("pages/performance.py", "My Performance"),
        Page("pages/admin.py", "Admin"),
        Section(name="Math Drill", icon=':books:'),
        Page("pages/menu.py", "Menu"),
        Page("pages/practice.py", "Question"),
        Page("pages/graded.py", "Graded Result"),
        Page("pages/chatbot.py", "Chat with ai", ':question:')
    ]
)

# when the user first logs in, session_state is initialized
# when the user logs out, session_state is reset
def session_state_reset():
	#student info
	st.session_state['student_id'] = None
	st.session_state['account'] = None
	st.session_state['name'] = None
	st.session_state['login'] = False
	st.session_state['teacher'] = False
	st.session_state['admin'] = False
	st.session_state['problem_id'] = None 
	
	# chatbot
	st.session_state['api_key'] = None
	st.session_state['openai_model'] = None
	st.session_state['message'] = []
	st.session_state['gpt_session'] = False
	st.session_state['gpt_client'] = None

# after login, session_state is initialized by student info from the database
def session_state_login_init(account):
	student_info = db.get_student_info_by_account(account)
	student_id = student_info['student_id'][0]

	st.session_state['login'] = True
	st.session_state['account'] = account
	st.session_state['name'] = student_info['name'][0]
	st.session_state['student_id'] = student_id
	if db.is_admin(student_id):
		st.session_state['admin'] = True
        
# session state initialization
if 'login' not in st.session_state: # should be changed to more clever way
	print(datetime.datetime.now(), "init session state")
	session_state_reset()

def __init__(self):
	self.apps = []
	
def add_app(self, title, function):
	self.apps.append({
		"title": title,
		"function": function
	})

def logout_callback():
    print(datetime.datetime.now(), 'logout callback')
    session_state_reset()

# TODO: main page contents
# Logo
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

encoded_image_1 = get_image_as_base64("mainpage_logo.png")

st.markdown(
    f"""
    <center>
        <img src="data:image/png;base64,{encoded_image_1}" width="300" style="margin-bottom: 20px;">
    </center>
    """,
    unsafe_allow_html=True
)

# Introduction 1
encoded_image_2 = get_image_as_base64("main_image_4.png")
st.markdown(
    f"""
    <style>
    @font-face {{
        font-family: 'Dolbomche_R';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2104@1.0/Dolbomche_R.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'SBAggroB';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/SBAggroB.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'MyLotteBold';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.0/MyLotteBold.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }}
    </style>

    <div style="display: flex; align-items: center; justify-content: flex-end; gap: 20px;">
        <div style="flex-grow: 1; text-align: left;">
            <p style="margin-bottom: 0px;">
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 30px;">논 · 서 · 구술형 평가 대비는</span><br>
                <span style="font-family: 'SBAggroB', sans-serif; font-size: 42px; color: #3A3A3A;">ERD</span>
                <span style="font-family: 'MyLotteBold', sans-serif; font-size: 40px; color: #3A3A3A;">!</span>
            </p>
        </div>
        <img src="data:image/png;base64,{encoded_image_2}" width="300" style="border-radius: 10px; margin-bottom: 50px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Introduction 2
encoded_image_3 = get_image_as_base64("main_image_7.png")
st.markdown(
    f"""
    <style>
    @font-face {{
        font-family: 'Dolbomche_R';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2104@1.0/Dolbomche_R.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'SBAggroB';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/SBAggroB.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }}
    </style>

    <div style="display: flex; align-items: center; justify-content: flex-start; gap: 20px;">
        <img src="data:image/png;base64,{encoded_image_3}" width="435" style="border-radius: 10px; margin-bottom: 70px;">
        <div style="flex-grow: 1; text-align: right;">
            <p style="margin-bottom: 0px;">
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 21px;"> 2022 개정 수학과 교육과정</span><br>
                <span style="font-family: 'JalnanGothic', sans-serif; font-size: 22px; color: #3A3A3A;">의사소통 역량</span><br><br>
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 21px;">2025 고교학점제</span><br>
                <span style="font-family: 'JalnanGothic', sans-serif; font-size: 22px; color: #3A3A3A;">미래형 교육 서비스 </span><br><br>
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 21px;">2028 대학입시제도 개편 시안 </span><br>
                <span style="font-family: 'JalnanGothic', sans-serif; font-size: 22px; color: #3A3A3A;">논 · 서술 평가 비중 상향 </span>
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Introduction 3
encoded_image_4 = get_image_as_base64("main_image_9.png")
st.markdown(
    f"""
    <center>
        <img src="data:image/png;base64,{encoded_image_4}" width="650" style="border-radius: 10px; margin-bottom: 10px;">
    </center>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <style>
    @font-face {{
    font-family: 'JalnanGothic';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_231029@1.1/JalnanGothic.woff') format('woff');
    font-weight: normal;
    font-style: normal;
    }}
    </style>
    <div style="text-align: center;">
        <p style="font-family: 'JalnanGothic', sans-serif; font-size: 28px; color: #3A3A3A; margin-bottom: 70px;">새로운 학습 과정, 어떻게 준비하고 계신가요?</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Feature Description
encoded_image_5 = get_image_as_base64("mainpage_logo3.png")
encoded_image_6 = get_image_as_base64("arrow.png")
st.markdown(
    f"""
    <center style="background-color: rgba(245, 245, 245, 0.5); padding: 10px; border-radius: 10px;">
        <img src="data:image/png;base64,{encoded_image_5}" width="105" style="border-radius: 10px; margin-bottom: 30px;">
        <p style="font-family: 'Dolbomche_R', sans-serif; font-size: 26px; color: #3A3A3A; margin-bottom: 2px;"> 새로운 학습 과정에 최적화된 ERD와 함께하세요!</p>
        <p style="font-family: 'Dolbomche_R', sans-serif; font-size: 22px; color: #3A3A3A; margin-bottom: 20px;"> 개인 맞춤 문제 추천부터 Ai 교사와 실시간 상호작용까지, 지금 경험해 보세요!</p>
        <img src="data:image/png;base64,{encoded_image_6}" width="45" style="border-radius: 10px; margin-bottom: 3px;">
    </center>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <center style="padding: 10px; border-radius: 10px;">
        <p style="font-family: 'Dolbomche_R', sans-serif; font-size: 50px;;"> </p>
    </center>
    """,
    unsafe_allow_html=True
)

#M1
encoded_image_7 = get_image_as_base64("main_m1.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: flex-start; justify-content: flex-end; gap: 20px;">
        <div style="flex-grow: 1; text-align: left;">
            <p style="margin-bottom: 20px;">
                <span style="font-family: 'JalnanGothic', sans-serif; font-size: 25px;">M1. 자동 채점 서비스</span><br>
            </p>
            <p style="margin-bottom: 10px;">
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 21px; color: #3A3A3A;"> 논·서·구술형 문제에 대한 새로운 접근 <br> 자동 채점 서비스를 경험해보세요.</span> 
            </p>
            <p style="margin-bottom: 0px;">
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 17px; color: #3A3A3A;"> Ai 교사가 교육과정 내의 지식요소를 활용하여 정확하게 채점합니다. <br> 더 이상 정답을 찾아 헤맬 필요가 없어요!</span>
            </p>
        </div>
        <img src="data:image/png;base64,{encoded_image_7}" width="390" style="border-radius: 10px; margin-bottom: 50px;">
    </div>
    """,
    unsafe_allow_html=True
)

#M2
encoded_image_8 = get_image_as_base64("main_m1.png")
st.markdown(
    f"""
    <div style="background-color: rgba(245, 245, 245, 0.5); display: flex; align-items: flex-end; justify-content: flex-end; gap: 20px; margin-bottom: 50px;"> 
        <img src="data:image/png;base64,{encoded_image_8}" width="390" style="border-radius: 10px; margin-bottom: 10px; margin-top: 10px;"> 
        <div style="text-align: left; margin-bottom: 20px;"> 
            <div style="margin-top: 0px;">
                <p style="margin-bottom: 20px;">
                    <span style="font-family: 'JalnanGothic', sans-serif; font-size: 25px;">M2. 상호작용 챗봇 서비스</span><br>
                </p>
                <p style="margin-bottom: 10px;">
                    <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 21px; color: #3A3A3A;"> 의사소통 능력을 키우고 싶으신가요? <br> 챗봇과의 대화를 통해 연습해보세요.</span> 
                </p>
                <p style="margin-bottom: 0px;">
                    <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 17px; color: #3A3A3A;"> 실시간 상호작용으로 의사소통 역량을 효과적으로 개발할 수 있습니다! </span>
                </p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#M3
encoded_image_9 = get_image_as_base64("main_m1.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: flex-start; justify-content: flex-end; gap: 20px;">
        <div style="flex-grow: 1; text-align: left;">
            <p style="margin-bottom: 20px;">
                <span style="font-family: 'JalnanGothic', sans-serif; font-size: 25px;">M3. 연습문제 추천 서비스</span><br>
            </p>
            <p style="margin-bottom: 10px;">
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 21px; color: #3A3A3A;"> 틀린 문제 뒤에 숨겨진 지식요소를 발견하고 싶으신가요? <br> ERD는 지식요소 레이블링을 활용해 <br> 여러분이 놓친 부분을 정밀하게 분석합니다.</span> 
            </p>
            <p style="margin-bottom: 0px;">
                <span style="font-family: 'Dolbomche_R', sans-serif; font-size: 17px; color: #3A3A3A;">맞춤형 연습문제로 실력을 한 단계 업그레이드해보세요!</span>
            </p>
        </div>
        <img src="data:image/png;base64,{encoded_image_9}" width="390" style="border-radius: 10px; margin-bottom: 50px;">
    </div>
    """,
    unsafe_allow_html=True
)


# the main page
if st.session_state["login"] == False:	# if not logged in
	# login box
	with st.form("main"):
			st.write("Login Page")
			account = st.text_input('ID:', autocomplete="on", placeholder="아이디 입력", max_chars=10)
			password = st.text_input('Password:', type='password', placeholder="비밀번호 입력", max_chars=4)			
			submitted = st.form_submit_button("로그인")
    
			# if login button is clicked,
			# 1. check whether student_id and password are not empty
			# 2. check whether (student_id, password) pair is in the database (in function db.login_user)
			# 3. if yes, 
			#		initialize session_state by calling session_state_login_init(student_id)
			# 4. switch page to info page (default page)

			if submitted:
				if account and password:
					
					login = db.login_user(account, password)
					if login:
						session_state_login_init(account)
						st.success("로그인 중")
						
						time.sleep(1) # redirect to info page after few seconds
						switch_page('my info')
    
					else: # if login fails
						st.error("ID 혹은 비밀번호를 다시 입력해주세요")
				else: # if student_id or password is empty
					st.error("모든 정보를 입력해주세요")
	if st.button("회원가입"):
		switch_page('signup')


else: # if logged in
    
	# show login status
    st.write("로그인 중", "ID:", st.session_state["name"])
	# show logout button
    if st.button('로그아웃'):
        logout_callback()
        switch_page('home')

link = '[GitHub](https://github.com/jean-jsj/ai-edtech/)'
st.markdown(link, unsafe_allow_html=True)