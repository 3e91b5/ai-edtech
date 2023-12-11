
import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date
import pandas as pd
import numpy as np
import src.db as db
import streamlit_extras.switch_page_button as switch_page
 
### 디자인 변경
# 좌측 상단 progress bar 디자인 변경
st.markdown("""
<style>
.stProgress > div > div > div > div {
    background-image: linear-gradient(to right, #808080 , #36454F);
}
</style>""",
unsafe_allow_html=True,
)

### 화면 구성
if 'login' in st.session_state:
    if st.session_state['login'] == True:

        student_id =  st.session_state['student_id']
        history = db.get_all_score(student_id)

        # NOTE: datetime object is different from date object (despite both being '2023-11-27')
        # both datetime(2023,11,27) and datetime.now() returns a datetime object
        # both date(2023,11,27) and date.today() returns a date object
        today = date.today()
        now = datetime.now()
        today = history[history['timestamp']==today][['problem_id','score']]
        
        history = pd.pivot_table(
            history,
            index='timestamp',
            aggfunc={'score': np.mean, 'problem_id': len}
        ).rename(columns={'problem_id': 'count'}).apply(np.ceil).round(decimals = 1) # round decimal (np.mean)
        history.reset_index(inplace=True)
        # NOTE: data import할 때 datetime 형식으로 데이터가 로드되지 않음. AttributeError: Can only use .dt accessor with datetimelike values
        history['timestamp'] = pd.to_datetime(history['timestamp'], format='%Y-%m-%d')
        history['week'] = history['timestamp'].dt.week
  
        conditions = [ 
          (history['timestamp'].dt.dayofweek == 0),
          (history['timestamp'].dt.dayofweek == 1),
          (history['timestamp'].dt.dayofweek == 2),
          (history['timestamp'].dt.dayofweek == 3),
          (history['timestamp'].dt.dayofweek == 4),
          (history['timestamp'].dt.dayofweek == 5),
          (history['timestamp'].dt.dayofweek == 6)
          ]

        values = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        history['Day of Week'] = np.select(conditions, values)

        # NOTE: now는 datetime object라 isocalendar()로 week number 계산. now.week하면 AttributeError: 'datetime.datetime' object has no attribute 'week'
        week = history[history['week'] == now.isocalendar()[1]][['Day of Week','count']]
        week.set_index("Day of Week", inplace = True)

        # NOTE: streamlit-calendar에선 날짜를 string 타입으로 넣어야 함
        history['timestamp'] = history['timestamp'].astype(str)

        calendar_options = {
            "headerToolbar": {
                "left": "today",
                "center": "title",
                "right": "prev,next",
            },
        }
        calendar_events = []
        for i in range(len(history['timestamp'])):
            # 푼 문항 수가 n개 이상이면 진한 회색, 미만이면 옅은 회색
            if history['count'][i] < 5:
                color = "#808080"
            else:
                color = "#36454F"

            title = '{:.0f}문제({:.0f}/10점)'.format(history['count'][i], history['score'][i])

            dict = {
                "title": title,
                "start": history['timestamp'][i],
                "end": history['timestamp'][i],
                "color": color,
            }
            calendar_events.append(dict)

        st.header('오늘의 학습 현황')
        column1, padding, column2 = st.columns((10,2,10))

        with column1:
            st.subheader('얼마나 정확하게 풀었나요?')
            st.data_editor(
            today, 
            column_config={
                "problem_id": "문항 번호", 
                "score": st.column_config.ProgressColumn( 
                    "문항별 점수 (10점 만점)",
                    format="%.1f",
                    min_value=0,
                    max_value=10,
                ),
            },
            hide_index=True,
            )
        with column2:
            st.subheader('얼마나 많이 풀었나요?')
            st.bar_chart(week, color = "#FF6C6C")
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
            switch_page("home")
else:
    st.write("로그인이 필요합니다.")
    clicked = st.button("main")
    if clicked:
        switch_page("home")
