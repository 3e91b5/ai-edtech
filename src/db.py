import psycopg2
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
from langchain.utilities import SQLDatabase
# import os

import warnings
warnings.filterwarnings("ignore")

def init_connection():
  connection = psycopg2.connect(
  user = st.secrets['username'],
  password = st.secrets['password'],
  host = st.secrets['host'],
  port = st.secrets['port'],
  database = st.secrets['database'])
  return connection

def init_db(include_tables = []):
    user = st.secrets['username']
    password = st.secrets['password']
    host = st.secrets['host']
    port = st.secrets['port']
    database = st.secrets['database']

    # Create the PostgreSQL URI used for connection
    pg_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    # Create the SQLDatabase object
    if include_tables == []:
        db = SQLDatabase.from_uri(pg_uri)
    else:
        db = SQLDatabase.from_uri(pg_uri, include_tables=include_tables,sample_rows_in_table_info=2)

    return db, pg_uri

def run_query(query):
  global conn
  conn = init_connection()
  try:
    df = pd.read_sql(query, conn)
  except psycopg2.Error as e:
    print(datetime.now(), "DB error: ", e)
    conn.close()
  finally:
    conn.close()
  return df

def run_tx(query):
  global conn
  conn = init_connection()
  try:
    with conn.cursor() as cur:
      cur.execute(query)
  except psycopg2.Error as e:
    print(datetime.now(), "DB error: ", e)
    conn.rollback()
    conn.close()
  finally:
    conn.commit()
    conn.close()
  return

################## Table: student_db.students ##################
# student_id: primary key
# account: unique
# password:
# admin: boolean
# name:
# age:
# date_joined:
# last_login:
# grade:
#################################################################

# 1. ACCOUNT / PERFORMANCE PAGE ----------------------------------------------------------------------------------------------- #
### GET INFO ###

# get student info by student_id
# result: Dataframe[student_id, account, password, admin, name, age, date_joined, last_login, grade]
def get_student_info(student_id):
	query = f"SELECT * FROM student_db.students WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# get student info by account
# result: student_id, account, password, admin, name, age, date_joined, last_login, grade
def get_student_info_by_account(account):
	query = f"SELECT * FROM student_db.students WHERE account = '{account}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

def view_all_users():
	query = 'SELECT * FROM student_db.students'
	result = run_query(query)
	return result

def is_admin(student_id):
	query = f"SELECT admin FROM student_db.students WHERE student_id = '{student_id}'"
	result = run_query(query)
	# print(datetime.now(), "is_admin",  result['admin'][0])

	if result['admin'][0] == True:
		return True
	else:
		return False


# output = dataframe with three columns (problem id - score - date when student solved the problem)
# 범위 = 여태까지 푼 모든 문제 히스토리
def get_all_score(student_id):
	query = f"SELECT problem_id, total_score, timestamp FROM student_db.problem_progress WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = scalar value that indicates the average "score" of 해당 student
# 범위 = 여태까지 푼 모든 문제 히스토리
def get_average_score(student_id):
	query = f"SELECT AVG(total_score) FROM student_db.problem_progress WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = scalar value that indicates the score for 해당 problem id
def get_score(student_id, problem_id):
	query = f"SELECT total_score FROM student_db.problem_progress WHERE student_id = '{student_id}' and problem_id = '{problem_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = list of elements that indicate the average "score" of 해당 student - 해당 sub_unit
# 범위 = input으로 들어온 sub_unit
def get_subunit_score(student_id):
	return

# output = list of elements that indicates the average "score" of 해당 student - 해당 main_unit
# 범위 = input으로 들어온 main_unit
def get_mainunit_score(student_id):
	return

# output = list of elements that indicates the average "score" of 해당 student - 해당 area
# 범위 = input으로 들어온 area
def get_area_score(student_id):
	return

# output = list of elements that indicates the average "score" of 해당 student - 해당 subject
# 범위 = input으로 들어온 subject
def get_subject_score(student_id):
	return

# output = list of elements (1 or 0) that indicate whether student "completed" each sub-unit (소단원)
# we use unit_id for sub unit ID and main_unit_id for main unit ID
def get_subunit_progress(student_id):
	query = f"SELECT unit_id FROM student_db.unit_progress WHERE student_id = '{student_id}' and achievement = 1"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = list of elements (1 or 0) that indicate whether student "completed" each main-unit (대단원)
# we use unit_id for sub unit ID and main_unit_id for main unit ID
# student "completes" main_unit iff he / she "completes" all sub_units included in the main_unit
def get_mainunit_progress(student_id):
	query = f"SELECT main_unit_id FROM student_db.unit_progress WHERE student_id = '{student_id}' and achievement = 1"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = list of elements (1 or 0) that indicate whether student "completed" each area
# student "completes" area iff he / she "completes" all main_units included in the area
def get_mainunit_progress(student_id):
	query = f"SELECT area_id FROM student_db.area_progress WHERE student_id = '{student_id}' and achievement = 1"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = list of elements (1 or 0) that indicate whether student "completed" each subject
# student "completes" subject iff he / she "completes" all area included in the subject
def get_mainunit_progress(student_id):
	query = f"SELECT subject_id FROM student_db.subject_progress WHERE student_id = '{student_id}' and achievement = 1"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = dataframe with five columns (subject / area / main unit / sub unit / progress)
# "progress" is a continuous variable from 0 to 1, which indicates the proportion of questions solved within the sub-unit
# 위 함수들은 progress를 완료 vs. 미완료로 정의. 반면 이 함수에선 각 unit / area / subject 에 속한 문제 중 몇 % 풀었는지로 정의. 
def get_progress(student_id):
	grade = get_student_grade(student_id)
	# query = f"SELECT knowledge_map_db.subject.subject_name, knowledge_map_db.area.area_name, knowledge_map_db.main_unit.main_unit_name, 
	# knowledge_map_db.sub_unit.unit_name, knowledge_map_db.problem.problem_id
	# FROM knowledge_map_db.subject
	# INNER JOIN knowledge_map_db.area
	# ON knowledge_map_db.subject.subject_id = knowledge_map_db.area.subject_id
	# INNER JOIN knowledge_map_db.main_unit
	# ON knowledge_map_db.area.area_id = knowledge_map_db.main_unit.area_id
	# INNER JOIN knowledge_map_db.sub_unit
	# ON knowledge_map_db.main_unit.main_unit_id = knowledge_map_db.sub_unit.main_unit_id
	# INNER JOIN knowledge_map_db.problem
	# ON knowledge_map_db.sub_unit.unit_id = knowledge_map_db.problem.unit_id
	# WHERE grade = '{grade}'"
	query = f"SELECT knowledge_map_db.subject.subject_name, knowledge_map_db.area.area_name, knowledge_map_db.main_unit.main_unit_name, knowledge_map_db.sub_unit.unit_name, knowledge_map_db.problem.problem_id FROM knowledge_map_db.subject INNER JOIN knowledge_map_db.area	ON knowledge_map_db.subject.subject_id = knowledge_map_db.area.subject_id INNER JOIN knowledge_map_db.main_unit ON knowledge_map_db.area.area_id = knowledge_map_db.main_unit.area_id INNER JOIN knowledge_map_db.sub_unit ON knowledge_map_db.main_unit.main_unit_id = knowledge_map_db.sub_unit.main_unit_id INNER JOIN knowledge_map_db.problem ON knowledge_map_db.sub_unit.unit_id = knowledge_map_db.problem.unit_id WHERE grade = '{grade}'"
	result = run_query(query)
	if result.empty:
		return False
	
	# compute proportion of questions solved for each sub-unit
	result = get_history(result, student_id)
	result = pd.pivot_table(
		result,
		index = 'unit_name',
		aggfunc = {'solved': np.sum, 'problem_id': len}
	).rename(columns = {'problem_id': 'total'})

	# convert pivot table to data frame
	result.reset_index(inplace = True)

	return result

# get student's knowledge progress -> TBD
def get_knowledge_progress(student_id):
	return

# get student's competence level -> TBD
def get_competence(student_id):
	return 


### UPDATE INFO ###

# add user to db when user sign up
# input: account, password, name, age, grade
# default value: admin = False, date_joined = datetime.now(), last_login = None
# return True if success, False if fail
def add_user(account, password, name, age, grade):
	query = f"SELECT * FROM student_db.students WHERE account = '{account}'"
	# print(datetime.now(), "check query:", query)
	result = run_query(query)

	if result.empty:
		# print(datetime.now(), "user data를 추가합니다.", account, password)
		date_joined = datetime.now()
		# student_id is auto-incremented, so no need to specify student_id
		add_query = f"INSERT INTO student_db.students (account, password, admin, name,age, grade,date_joined) VALUES('{account}', '{password}', False,'{name}', '{age}', '{grade}', '{date_joined}')"

		run_tx(add_query)
		return True
	else:
		return False

# check if user exists in db when user login
# if user exists, update last_login field and return True
def login_user(account, password):
	query = f"SELECT * FROM student_db.students WHERE account = '{account}' AND password = '{password}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		last_login = datetime.now()
		student_id = result['student_id'][0]
		# update last_login field
		query = f"UPDATE student_db.students SET last_login = '{last_login}' WHERE student_id = '{student_id}'"
		run_tx(query)
		return True


# admin function for deleting user
#### WARNING ####
# this function does not have double check for deleting user
def delete_user(student_id):
	query = f"select * from student_db.students where student_id = '{student_id}'"
	result = run_query(query)
	if result.empty: # user not found
		return False
	account = result['account'][0]
	query = f"DELETE FROM student_db.students WHERE student_id = '{student_id}'"
	run_tx(query)
	# print(datetime.now(), "delete user", account)
	
	return True


# set user password
def set_user_password(student_id, new_password):
	query = f"UPDATE student_db.students SET password = '{new_password}' WHERE student_id = '{student_id}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True


# 2. MENU PAGE ------------------------------------------------------------------------------------------------------------ #

def init_knowledge_str():
	connection = init_connection()
	cursor = connection.cursor()
	query = "SELECT knowledge_id, knowledge_name FROM knowledge_map_db.knowledge;"
	cursor.execute(query)
	knowledge_table = 'knowledge_map_db.knowledge'
	knowledge_columns = [description[0] for description in cursor.description]
	knowledge_data = cursor.fetchall()
	knowledge_str = f"{knowledge_table}, {knowledge_columns}, {knowledge_data}"
	return knowledge_str

# student_db.students 에서 각 정보를 가져오는 함수를 따로 짤 수도 있지만 get_student_info를 재사하는 방법도 있음
def get_student_grade(student_id):
	return get_student_info(student_id)['grade'][0]

# output = scalar value that indicates student's school grade (학년)
# def get_student_grade(student_id):
# 	query = f"SELECT grade FROM student_db.students WHERE student_id = '{student_id}'"
# 	result = run_query(query)
# 	if result.empty:
# 		return False
# 	else:
# 		return result['grade'][0]

# output = list of unit name that matches student's grade (학년)
# Menu 화면 display 용도
def get_main_unit_name(grade):
	query = f"SELECT main_unit_name FROM knowledge_map_db.main_unit WHERE grade = {grade}"
	# query = f"""
	# SELECT knowledge_map_db.main_unit.main_unit_name FROM knowledge_map_db.main_unit 
	# INNER JOIN knowledge_map_db.sub_unit
	# ON knowledge_map_db.main_unit.main_unit_id = knowledge_map_db.sub_unit.main_unit_id
	# INNER JOIN knowledge_map_db.knowledge
	# ON knowledge_map_db.sub_unit.sub_unit_id = knowledge_map_db.knowledge.sub_unit_id
	# WHERE grade = '{grade}'
	# """
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = list of unit name that matches student's grade (학년)
# Menu 화면 display 용도
def get_sub_unit_name(grade):
	query = f"SELECT sub_unit_name FROM knowledge_map_db.sub_unit WHERE grade = {grade}"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = list of unit name that matches student's grade (학년)
# Menu 화면 display 용도
def get_knowledge_name(grade):
#	query = f"SELECT knowledge_name FROM knowledge_map_db.knowledge WHERE grade = {grade}"
	query = f"""
	SELECT knowledge_map_db.knowledge.knowledge_name FROM knowledge_map_db.knowledge 
	INNER JOIN knowledge_map_db.sub_unit
	ON knowledge_map_db.knowledge.sub_unit_id = knowledge_map_db.sub_unit.sub_unit_id
	WHERE grade = '{grade}'
	"""
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = id that corresponds to the name selected 
# name을 id로 바꾼 후 get_problem_list()에 input으로 넣을 용도
def get_knowledge_id(knowledge_name):
	query = f"SELECT knowledge_id FROM knowledge_map_db.knowledge WHERE knowledge_name = '{knowledge_name}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result
	
def get_problem_list(knowledge_id):
	query = f"SELECT problem_id FROM knowledge_map_db.problem WHERE knowledge_id = '{knowledge_id}' ORDER BY problem_id"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

def get_problem(problem_id):
    # connection = init_connection()
    # cursor = connection.cursor()

	p_query = """
	SELECT
		*
	FROM
		knowledge_map_db.problem
	WHERE
		problem_id = {}
	LIMIT 1;
	""".format(problem_id)

	result = run_query(p_query)
	if result.empty:
		return False
	else:
		return result
		# question = result['question'][0]
		# knowledge = result['knowledge_score'][0]
		# return question, knowledge
	# 	return ques
    # try:
    #     cursor.execute(p_query)
    #     p_query_data = cursor.fetchall()
    #     question = p_query_data[0][0]
    #     knowledge = p_query_data[0][1]
    # except (Exception, psycopg2.Error) as error:
    #     print("Error while connecting to PostgreSQL", error)
    #     connection.rollback()
    # return question, knowledge

def get_answer(student_id, problem_id):

	s_query = """
	SELECT
		student_answer
	FROM
		student_db.problem_progress
	WHERE
		student_id = {} AND
		problem_id = {}
	ORDER BY
		Timestamp DESC
	LIMIT 1;
	""".format(student_id, problem_id)

	result = run_query(s_query)
	if result.empty:
		return False
	else:
		student_answer = result['student_answer'][0]
		return student_answer
    # cursor.execute(s_query)
    # s_query_data = cursor.fetchall()
    # student_answer = s_query_data[0][0]

    # print(student_answer)
    # return student_answer\
        
# output = list of problem_id that 해당 student previously worked on
# Menu 페이지에서 버튼 색상 구현할 때 사용
def get_history(df, student_id):
	l = df['problem_id'].tolist()
	solved = []
	query = f"SELECT problem_id FROM student_db.problem_progress WHERE student_id = '{student_id}'"
	result = run_query(query)
	
	for q in l:
		if q in result['problem_id']:
			solved.append(1)
		else:
			solved.append(0)

	return solved

# 3. QUESTION PAGE --------------------------------------------------------------------------------------------------------- #

# output = list of five values that indicate student's competence level for each 역량 요소
def get_student_competence(student_id):
	query = f"SELECT competence FROM student_db.student_competence WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# output = one row of dataframe selected if problem_id is equal to what is (i) selected by the student or (ii) recommended by the system
# output에 "정답" 답안지 및 배점 포함되어 있음. Question page, Graded result page 모두에서 사용하는 함수.
def get_selected_problem(problem_id):
	query = f"SELECT * FROM knowledge_map_db.problem WHERE problem_id = '{problem_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

'''
# neo4j (지식요소 겹치는 문제들 연결 - 같은 단원 내로 한정)
def get_related_problems(qid):
	query = f"MATCH ({qid : $qid})-[*]-(connected) RETURN connected"
	return

# neo4j (역량요소별로.. 배점 제일 높은 문제들 연결)
def get_capacity_problems(cid):
	return

# 추천 문제 제시
def get_recommend_problem(unit_id, student_id, problem_id):
	# 같은 단원 & 지식 요소 1개 이상 겹치는 문제들 가져옴
	problems = get_related_problems(problem_id)
	# 학생이 각 문제 풀었는지 확인 (풀었으면 solved = 1, 안 풀었으면 solved = 0)
	cond1 = get_history(problems, student_id)
	# 학생의 역량 요소 중 점수가 가장 낮은 요소 확인
	capacity = get_student_capacity(student_id)
	cid = capacity.iloc[0].idxmin()
	cond2 = get_capacity_problems(cid)

	df = pd.concat([problems, cond1, cond2], axis=1, join='outer') # concat 맞나?
	df = df.drop(df[(df.cond1 == 1) | (df.cond2 == NaN)].index)

	# 문제가 2개 이상 남은 경우 첫번째 문제 선택
	if len(df.index) > 1:
		nqid = df['qid'][0]
	elif len(df.index) == 1:
		nqid = df['qid']
	else:
		return False

	return nqid
'''

# 4. GRADED RESULTS PAGE ---------------------------------------------------------------------------------------------------- #

# if student leaves page without clicking on "제출하기", uploaded files are removed (예: Menu, My Performance, Admin page 방문했다가 돌아옴)
# 학생이 "제출하기" 누르면
#	1) gpt.py 의 get_ocr() 함수 call. converted file을 input으로 받고, output은 latex. db 저장하지 않고 바로 grade_answer()의 input으로.
#	2) gpt.py 의 grade_answer() 함수 call. output은 graded answer (latex, 부분 점수)
#	3) db.py의 update_graded_answer() 함수 call. 결과를 db에 저장.

# update answer (and score) graded by chatGPT 
# update 시점: "제출하기" 버튼 누른 직후
def update_graded_answer(problem_id, student_id, solved_answer):
	today = date.today()
	query = f"INSERT INTO student_db.problem_progress VALUES ('{student_id}', '{problem_id}', {solved_answer}, {today})"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True

# output = dataframe with three columns (student_answer, step_score, total_score)
# 		   dataframe rows are selected based on conditions: problem_id solved by the student
# "학생이 작성한" 답안지 가져오는 쿼리
# def get_answer(problem_id, student_id):
# 	query = f"SELECT student_answer, knowledge_score, score FROM student_db.problem_progress WHERE problem_id = '{problem_id}' and student_id = '{student_id}' "
# 	result = run_query(query)
# 	if result.empty:
# 		return False
# 	else:
# 		return result

# 5. CHAT WITH AI PAGE ---------------------------------------------------------------------------------------------------- #

# Chat with AI 할때 가져갈 정보 -> TBD
def get_chat():
	return

# chat 했으면 그 내용 update -> TBD
def update_chat():
	return

# 6. session logout 한 직후 database update --------------------------------------------------------------------------------- #

# update할 사항:
# 1) subject / area / main unit / sub unit 별 progress (해당하는 문제들 전부 풀었는지 여부)
# 2) 역량, 지식 요소 progress 
# subject / area / main unit / sub unit 별 평균 성적은 따로 db에 저장하지 않고, 필요시 쿼리로 계산

# update progress (value 0 if incomplete, 1 if complete) for each sub-unit (소단원)
# "completion" indicates that the student solved all questions within each unit
def update_subunit_progress(student_id):
	return

# update progress (value 0 if incomplete, 1 if complete) for each main-unit (대단원)
def update_mainunit_progress(student_id):
	return 

# update progress (value 0 if incomplete, 1 if complete) for each area
def update_area_progress(student_id):
	return 

# update progress (value 0 if incomplete, 1 if complete) for each subject
def update_subject_progress(student_id):
	return

# update student's level of competence for each 역량 요소
def update_student_competence(student_id):
	return
	
# update student's progress for each 지식 요소
def update_student_knowledge(student_id, knowledge_id):
	return



################## Table: student_db.student_competence ##################
# student_competence_id: primary key
# student_id: foreign key
# competence:
# competence_id:
##########################################################################

################## Table: student_db.problem_progress ##################
# problem_progress_id: primary key
# student_id: foreign key
# problem_id: foreign key
# student_answer:
# step_score:
# total_score:
# correctness:
# feedback:
# timestamp:
##########################################################################

################## Table: student_db.unit_progress ##################
# unit_progress_id: primary key
# student_id: 
# main_unit_id: 
# unit_id: 
# achievement:
##########################################################################


################## Table: knowledge_map_db.problem ##################
# student_competence_id: primary key
# student_id: foreign key
# competence:
# competence_id:
##########################################################################

