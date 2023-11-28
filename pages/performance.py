import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd
import numpy as np
import src.db as db
import streamlit_extras.switch_page_button as switch_page
now = datetime.now()
dt = now.strftime("%Y-%m-%d")
from st_pages import show_pages_from_config, add_page_title
# add_page_title()
# show_pages_from_config()



if 'login' in st.session_state:
    if st.session_state['login'] == True:
        ### toy data 사용 
        data_df = pd.DataFrame(
            {
                "question": ['Q101','Q102','Q103','Q104','Q105'],
                "score": [20, 95, 55, 80, 64],
            }
        )
        from PIL import Image
        image1 = Image.open('pages/performance1.jpg')
        st.image(image1, use_column_width=True, caption='demo1')
        image2 = Image.open('pages/performance2.jpg')
        st.image(image2, use_column_width=True, caption='dem21')
        
        ### 변수 가져오기
        student_id =  st.session_state['student_id']
        # st.write('student_id: ', student_id)
        history = db.get_all_score(student_id) 
        # st.write('history: ', history)
        today = history[history['timestamp'] == dt]
        # st.write('today', today)
        # st.write('len(history): ', len(history))
        history = pd.pivot_table(
            history,
            index=['timestamp'],
            aggfunc={'total_score': np.sum,
                    # 'student_id': st.session_state['student_id']
                    },
            # columns=['count'],
        ).rename(columns={'student_id': 'count'}) 
        history['week'] = history['timestamp'].isocalendar()[1]
        week = history[history['week'] == dt.isocalendar()[1]][['timestamp','count']]
        # history['timestamp'] = history['timestamp'].astype(str)

        ### 좌측 상단 progress bar 디자인 변경
        st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-image: linear-gradient(to right, #808080 , #36454F);
                }
            </style>""",
            unsafe_allow_html=True,
        )

        ### calendar detail
        calendar_options = {
            "headerToolbar": {
                "left": "today",
                "center": "title",
                "right": "prev,next",
            },
        }
        calendar_events = []
        for i in range(len(history)):
            # 푼 문항 수가 n개 (기준 임의로 설정?) 이상이면 진한 회색, 미만이면 옅은 회색
            if history['count'][i] < 5:
                color = "#808080"
            else:
                color = "#36454F"

            dict = {
                "title": '성취도: {0}%'.format(history['total_score'][i]),
                "start": history['timestamp'][i],
                "end": history['timestamp'][i],
                "color": color,
            }    
            calendar_events.append(dict)

        ### 화면 구성
        st.header('오늘의 학습 현황')
        column1, padding, column2 = st.columns((10,2,10))

        with column1:
            st.subheader('얼마나 정확하게 풀었나요?')
            st.data_editor(
            data_df, # data_df -> today로 수정 
            column_config={
                "question": "문항 번호", # question -> problem_id로 수정
                "score": st.column_config.ProgressColumn( # score -> total_score로 수정
                    "문항별 점수 (100점 만점)",
                    format="%f",
                    min_value=0,
                    max_value=100,
                ),
            },
            hide_index=True,
            )
        with column2:
            st.subheader('얼마나 많이 풀었나요?')
            #st.line_chart(week.rename(columns={'timestamp':'index'}).set_index('index'))
        st.markdown('***')

        st.header("월별 학습 현황")
        calendar = calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
            """,
        )

        st.write(calendar)
    else:
        st.write("로그인이 필요합니다.")
        clicked = st.button("main")
        if clicked:
            switch_page("main")
else:
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("main")