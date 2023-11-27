import psycopg2
import streamlit as st
import pandas as pd
import datetime

import warnings
warnings.filterwarnings(action='ignore')

def init_connection():
    #### WARNING ####
    # database password should be removed before pushing to github
	return psycopg2.connect(f"host=147.47.200.145 dbname=teamdb3 user=team3 password={st.secrets['password']} port=34543")
	
def run_query(query):
    print(datetime.datetime.now(), 'run query:',  query)
    try:
        conn = init_connection()
        df = pd.read_sql(query, conn)
    except psycopg2.Error as e:
        print(datetime.datetime.now(), "DB error: ", e)
        conn.close()
    finally:
        conn.close()
    return df

def run_tx(query):
	print(datetime.datetime.now(), 'run tx:',  query)
	try:
		conn = init_connection()
		with conn.cursor() as cur:
			cur.execute(query)
	except psycopg2.Error as e:
		print(datetime.datetime.now(), "DB error: ", e)
		conn.rollback()
		conn.close()
	finally:
		conn.commit()
		conn.close()
	return

def get_student_info(account):
	query = f"SELECT * FROM student_db.students WHERE account = '{account}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 
def add_user(student_id, password, name, age, grade):
	query = f"SELECT * FROM student_db.students WHERE account = '{student_id}'"
	print(datetime.datetime.now(), "check query:", query)
	result = run_query(query)

	if result.empty:
		print(datetime.datetime.now(), "user data를 추가합니다.", student_id, password)
		date_joined = datetime.datetime.now()
		add_query = f"INSERT INTO student_db.students (account, password, admin, name,age, grade,date_joined) VALUES('{student_id}', '{password}', False,'{name}', '{age}', '{grade}', '{date_joined}')"

		run_tx(add_query)
		return True
	else:
		return False

def login_user(student_id,password):
	query = f"SELECT * FROM student_db.students WHERE account = '{student_id}' AND password = '{password}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		last_login = datetime.datetime.now()
		query = f"UPDATE student_db.students SET last_login = '{last_login}' WHERE account = '{student_id}'"
		run_tx(query)
		return True

def view_all_users():
	query = 'SELECT * FROM student_db.students'
	result = run_query(query)
	return result

def delete_user(student_id):
	query = f"select * from student_db.students where account = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	query = f"DELETE FROM student_db.students WHERE account = '{student_id}'"
	run_tx(query)
	print(datetime.datetime.now(), "delete user", student_id)
	
	return True

def is_admin(student_id):
	query = f"SELECT admin FROM student_db.students WHERE account = '{student_id}'"
	result = run_query(query)
	print(datetime.datetime.now(), "is_admin",  result['admin'][0])
	
	if result['admin'][0] == True:
		return True
	else:
		return False

def update_user_password(student_id, new_password):
	query = f"UPDATE student_db.students SET password = '{new_password}' WHERE account = '{student_id}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True
	
def update_student_score(student_id, score):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.		
	query = f"UPDATE edutech.studentdb SET score = '{score}' WHERE student_id = '{student_id}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True

##### student info #####
# school grade (학년)
def get_student_grade(student_id):
	query = f"SELECT grade FROM student_db.students WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 상/중/하 클래스
def get_student_level(student_id):
	query = f"SELECT level FROM student_db.students WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# competence (역량 요소)
def get_student_competence(student_id):
	query = f"SELECT competence FROM student_db.student_competence WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 모든 문제에 대한 score
def get_all_score(student_id):
	query = f"SELECT problem_id, total_score, timestamp FROM student_db.problem_progress WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 특정 문제 score
def get_score(student_id, problem_id):
	query = f"SELECT total_score FROM student_db.problem_progress WHERE student_id = '{student_id}' and problem_id = '{problem_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 소단원 평균 score -> unit_id는 sub unit ID 
def get_subunit_score(student_id, unit_id):
	query = f"SELECT achievement FROM student_db.unit_progress WHERE student_id = '{student_id}' and unit_id = '{unit_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 대단원 평균 score -> main_unit_id는 main unit ID 
def get_mainunit_score(student_id, main_unit_id):
	query = f"SELECT AVG(achievement) FROM student_db.unit_progress WHERE student_id = '{student_id}' and main_unit_id = '{main_unit_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result
	
# 전체 평균 score
def get_average_score(student_id):
	query = f"SELECT AVG(achievement) FROM student_db.unit_progress WHERE student_id = '{student_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result
	
##### 문제 풀이 페이지 구현 #####
# 학년별 list of units 
def get_units(grade):
	query = f"SELECT unit_id FROM knowledge_map_db.units WHERE grade = '{grade}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 학생이 선택한 단원 & 학생 클래스 기준으로 list of questions 가져옴
def get_problems():
	#def get_problems(unit_id, student_id):
	#level = get_student_level(student_id)
	#query = f"SELECT problem_id FROM knowledge_map_db.problem WHERE unit_id = '{unit_id}' AND level = '{level}"
	query = f"SELECT problem_id FROM knowledge_map_db.problem"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 학생이 선택한 문제 가져오기
def get_selected_problem(problem_id):
	query = f"SELECT * FROM knowledge_map_db.problem WHERE problem_id = '{problem_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 채점결과 페이지 구현시 답안지 가져오기
def get_solution(problem_id):
	query = f"SELECT solution, step_criteria, step_score FROM knowledge_map_db.problem WHERE problem_id = '{problem_id}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 채점결과 페이지 구현시 학생 답안 가져오기
def get_answer(problem_id, student_id):
	query = f"SELECT student_answer, step_score, total_score FROM knowledge_map_db.problem_progress WHERE problem_id = '{problem_id}' and student_id = '{student_id}'"
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

# # neo4j (역량요소별로.. 배점 제일 높은 문제들 연결)
# def get_capacity_problems(cid):
# 	query = 
# 	return 

# 추천 문제 제시
def recommend_problem(unit_id, student_id, problem_id):
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
##### 풀이 현황 업데이트 #####
# 각 문제를 학생이 기존에 푼적 있는지 여부 확인
def get_history(list, student_id): 
	solved = []
	query = f"SELECT problem_id FROM student_db.problem_progress WHERE student_id = '{student_id}'"
	result = run_query(query)
	for q in list:
		if q in result:
			solved.append(1)
		else:
			solved.append(0)
    
	return solved

# 채점 후 progress update -> 수정 필요
def update_answer(problem_id, student_id, step_score, total_score, answer):
	now = datetime.now()
	dt = now.strftime("%Y-%m-%d")
	query = f"INSERT INTO student_db.problem_progress VALUES ('{student_id}', '{problem_id}', {answer}, {step_score}, {total_score}, {dt})"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True

# 단원별 평균 성적 -> 학생 학년에 맞는 unit은 미리 입력해둠 
def update_unit_score(unit_id, student_id):
	query_1 = f"SELECT AVG(total_score) FROM student_db.problem_progress WHERE student_id = '{student_id}' and unit_id = '{unit_id}'"
	score = run_query(query_1)
	if score.empty:
		return False
 
	query_2 = f"UPDATE student_db.unit_progress SET achievement = '{score}' WHERE student_id = '{student_id}' and unit_id = '{unit_id}'"
	result = run_tx(query_2)
	if result.empty:
		return False
	else:
		return True
'''
# update competence db -> 수정 필요. competence의 initial value = 0
def update_competence(student_id, problem_id):
	# 방금 푼 문제 -> competence element 배점 확인
	query1 = f"SELECT competence FROM knowledge_map_db.problem WHERE problem_id = '{problem_id}'"
	proportion = run_query(query1)

	query2 = f"SELECT total_score FROM student_db.problem_progress WHERE student_id = '{student_id}'"
	score = run_query(query2)

	proportion = proportion * score
	# 기존 역량요소 값과의 평균으로 update 
	query3 = f"UPDATE student_db.student_competence 
			SET competence += CASE competence_id
							WHEN 1 THEN '{proportion[0]}' 
							WHEN 2 THEN '{proportion[1]}' 
							WHEN 3 THEN '{proportion[2]}' 
							WHEN 4 THEN '{proportion[3]}' 
							WHEN 5 THEN '{proportion[4]}'
							ELSE competence 
							END
							WHERE competence_id IN (1,2,3,4,5) and student_id = '{student_id}'"
	result = run_tx(query3)
	if result.empty:
		return False
	else:
		return True

# update knowledge db -> 위 함수와 동일한 방식으로 수정
def update_knowledge(student_id, knowledge):

	return 
'''