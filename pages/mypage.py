import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd
now = datetime.now()
dt = now.strftime("%Y-%m-%d")

### toy data 사용 (score: 성적, completion: 주어진 문제 중 몇 %를 풀었는지)
data_df = pd.DataFrame(
    {
        "question": ['Q101','Q102','Q103','Q104','Q105'],
        "score": [20, 95, 55, 80, 64],
    }
)

history = pd.read_excel('history.xlsx')
history['date'] = history['date'].astype(str)

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
    # completion rate가 50% 미만이면 옅은 회색, 50% 이상이면 진한 회색으로 표기
    if history['completion'][i] < 0.5:
        color = "#808080"
    else:
        color = "#36454F"
    if history['date'][i] == dt:
        progress = history['completion'][i]

    dict = {
        "title": '성취도: {0}%'.format(history['score'][i]),
        "start": history['date'][i],
        "end": history['date'][i],
        "color": color,
    }    
    calendar_events.append(dict)

### 화면 구성
st.header('오늘의 학습 현황')
column1, padding, column2 = st.columns((10,2,10))

with column1:
    st.subheader('얼마나 많이 풀었나요?')
    progress_percent = progress * 100
    st.progress(progress, text = f"{progress_percent}%")
with column2:
    st.subheader('얼마나 정확하게 풀었나요?')
    st.data_editor(
    data_df,
    column_config={
        "question": "문항 번호",
        "score": st.column_config.ProgressColumn(
            "문항별 점수 (100점 만점)",
            format="%f",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
    )

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