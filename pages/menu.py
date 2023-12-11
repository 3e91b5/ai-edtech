import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# import pandas as pd
import src.db as db
import src.app as app
import pandas as pd

PROBLEMS_PER_LINE = 3

if 'login' in st.session_state:
    if st.session_state['login'] == True:
        ### 변수 가져오기
        student_id = st.session_state['student_id']
        grade = db.get_student_grade(student_id)

        main_units = db.get_main_unit_name(grade)
        # sub_units = db.get_sub_unit_name(grade)
        sub_units = pd.DataFrame()
        # knowledges = db.get_knowledge_name(grade)
        knowledges = pd.DataFrame()
        ### 화면 구성
        st.header("학습메뉴")
        col1, padding= st.columns([3,1])
        # col2, col3, col4, col5 = st.columns([2,2,2,2])
        with col1:

            main_unit = st.selectbox(
                "대단원을 선택해주세요",
                main_units,
                index = None,
                placeholder = "단원명",
                )

            # should add code to change sub_units according to main_unit
            if main_unit != None:
                sub_units = db.get_sub_unit_name_by_main_unit(main_unit)
                sub_unit = st.selectbox(
                    "소단원을 선택해주세요",
                    sub_units,
                    index = None,
                    placeholder = "단원명",
                    )

                # should add code to change knowledge according to sub_unit
                if sub_unit != None:
                    knowledges = db.get_knowledge_name_by_sub_unit(sub_unit)
                    knowledge = st.selectbox(
                        "지식요소를 선택해주세요",
                        knowledges,
                        index = None,
                        placeholder = "단원명",
                        )

        if main_unit and sub_unit and knowledge:
            knowledge_id = db.get_knowledge_id(knowledge)['knowledge_id'][0]
            problem_list = db.get_problem_list(knowledge_id) # the list of problem_id which has the selected knowledge_id
            
            if problem_list is not False:
                problem_list = problem_list['problem_id'].tolist()
                problems = pd.DataFrame()
                for i in range(len(problem_list)):
                    problems = problems.append(db.get_problem(problem_list[i]), ignore_index=True)
                
                problems['solved'] = db.get_history(problems, student_id)   # append 'solved' column to problems dataframe
                
                # display problems in PROBLEMS_PER_LINE columns
                for line in range(len(problems['problem_id'])//PROBLEMS_PER_LINE):
                    cols = st.columns(PROBLEMS_PER_LINE)
                    for num in range(PROBLEMS_PER_LINE):
                        with cols[num]:
                            app.question_buttons(problems, line*PROBLEMS_PER_LINE + num)
                
                remain = len(problems['problem_id'])%PROBLEMS_PER_LINE
                line_num = len(problems['problem_id'])//PROBLEMS_PER_LINE
                remain_cols = st.columns(PROBLEMS_PER_LINE)
                for num in range(remain):
                    with remain_cols[num]:
                        app.question_buttons(problems, (line_num)*PROBLEMS_PER_LINE + num)
            else:
                st.error("해당 지식요소에 대한 문제가 없습니다.")
            
            
        else:
            st.write("대단원, 소단원, 지식요소를 전부 선택해주세요.")
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