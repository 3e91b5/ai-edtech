import psycopg2
import streamlit as st
import pandas as pd
import datetime

def init_connection():
    #### WARNING ####
    # database password should be removed before pushing to github
	return psycopg2.connect("host=147.47.200.145 dbname=teamdb3 user=team3 password=0 port=34543")
	
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

def add_user(sid,password):
	query = f"SELECT * FROM edutech.students WHERE sid = '{sid}'"
	result = run_query(query)

	if result.empty:
		print(datetime.datetime.now(), "user data를 추가합니다.", sid, password)
		add_query = f"INSERT INTO edutech.students (sid, password, admin) VALUES('{sid}', '{password}', False)"
		run_tx(add_query)
		return True
	else:
		return False

def login_user(sid,password):
	query =f"SELECT * FROM edutech.students WHERE sid ='{sid}' AND password = '{password}'"
	result = run_query(query)

	if result.empty:
		return False
	else:
		return True

def view_all_users():
	query = 'SELECT * FROM edutech.students'
	result = run_query(query)
	return result

def delete_user(sid):
	query = f"select * from edutech.students where sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	query = f"DELETE FROM edutech.students WHERE sid = '{sid}'"
	run_tx(query)
	print(datetime.datetime.now(), "delete user", sid)
	
	return True

def is_admin(sid):
	query = f"SELECT admin FROM edutech.students WHERE sid = '{sid}'"
	result = run_query(query)
	print(datetime.datetime.now(), "is_admin",  result['admin'][0])
	
	if result['admin'][0] == True:
		return True
	else:
		return False

def update_user_password(sid, new_password):
	query = f"UPDATE edutech.students SET password = '{new_password}' WHERE sid = '{sid}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True

##### student info #####
# school grade (학년)
def get_student_grade(sid):
	query = f"SELECT grade FROM edutech.students WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 상/중/하 클래스
def get_student_level(sid):
	query = f"SELECT level FROM edutech.students WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# capacity (역량 요소)
def get_student_capacity(sid):
	query = f"SELECT * FROM edutech.student_competence WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 특정 문제 score
def get_score(sid, qid):
	query = f"SELECT total_score FROM edutech.problem_progress WHERE sid = '{sid}' and qid = '{qid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 소단원 평균 score -> uid는 sub unit ID
def get_subunit_score(sid, uid):
	query = f"SELECT score FROM edutech.unit_progress WHERE sid = '{sid}' and uid = '{uid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 대단원 평균 score -> muid는 main unit ID
def get_mainunit_score(sid, muid):
	query = f"SELECT AVG(score) FROM edutech.unit_progress WHERE sid = '{sid}' and muid = '{muid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result
	
# 전체 평균 score
def get_average_score(sid):
	query = f"SELECT AVG(score) FROM edutech.unit_progress WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result
	
##### 문제 풀이 페이지 구현 #####
# 학년별 list of units 
def get_units(grade):
	query = f"SELECT * FROM edutech.units WHERE grade = '{grade}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 학생이 선택한 단원 & 학생 클래스 기준으로 list of questions 가져옴
def get_problems(uid, sid):
	level = get_student_level(sid)
	query = f"SELECT * FROM edutech.problem WHERE uid = '{uid}' AND level = '{level}"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 학생이 선택한 문제 가져오기
def get_selected_problem(qid):
	query = f"SELECT * FROM edutech.problems WHERE qid = '{qid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 채점결과 페이지 구현시 답안지 가져오기
def get_solution(qid):
	query = f"SELECT solution, step_criteria, step_score FROM edutech.problem WHERE qid = '{qid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# 채점결과 페이지 구현시 학생 답안 가져오기
def get_solved(qid, sid):
	query = f"SELECT student_answer, step_score, total_score FROM edutech.problem_progress WHERE qid = '{qid}' and sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# neo4j (지식요소 겹치는 문제들 연결 - 같은 단원 내로 한정)
def get_related_problems(qid):
	query = f"MATCH ({qid : $qid})-[*]-(connected) RETURN connected"
	return 

# neo4j (역량요소별로.. 배점 제일 높은 문제들 연결)
def get_capacity_problems(cid):
	query = 
	return 

# 추천 문제 제시
def recommend_problem(tid, sid, qid):
	# 같은 단원 & 지식 요소 1개 이상 겹치는 문제들 가져옴
	problems = get_related_problems(qid)
	# 학생이 각 문제 풀었는지 확인 (풀었으면 solved = 1, 안 풀었으면 solved = 0)
	cond1 = get_history(problems, sid)
	# 학생의 역량 요소 중 점수가 가장 낮은 요소 확인
	capacity = get_student_capacity(sid)
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

##### 풀이 현황 업데이트 #####
# 각 문제를 학생이 기존에 푼적 있는지 여부 확인
def get_history(list, sid): 
	solved = []
	query = f"SELECT qid FROM edutech.problem_progress WHERE sid = '{sid}'"
	result = run_query(query)
	for q in list:
		if q in result:
			solved.append(1)
		else:
			solved.append(0)
    
	return solved

# 문제 풀이 결과
def update_solved(qid, sid, score, solved):
	now = datetime.now()
	dt = now.strftime("%Y-%m-%d")
	total = sum(score)
	query = f"INSERT INTO edutech.problem_progress VALUES ('{sid}', '{qid}', {dt}, {total}, {score}, {solved})"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True

# 단원별 평균 성적 -> 학생 학년에 맞는 unit은 미리 입력해둠 
def update_unit_score(uid, sid):
	query_1 = f"SELECT AVG(total) FROM edutech.problem_progress WHERE sid = '{sid}' and uid = '{uid}'"
	score = run_query(query_1)
	if score.empty:
		return False
 
	query_2 = f"UPDATE edutech.unit_progress SET achievement = '{score}' WHERE sid = '{sid}' and uid = '{uid}'"
	result = run_tx(query_2)
	if result.empty:
		return False
	else:
		return True

# update 학생의 역량 요소 value -> input "capacity"는 list
def update_capacity(sid, capacity):
	query = f"UPDATE edutech.student_competence 
			SET competence = CASE cid
							WHEN 1 THEN '{capacity[0]}' 
							WHEN 2 THEN '{capacity[1]}' 
							WHEN 3 THEN '{capacity[2]}' 
							WHEN 4 THEN '{capacity[3]}' 
							WHEN 5 THEN '{capacity[4]}'
							ELSE competence 
							END
							WHERE cid IN (1,2,3,4,5) and sid = '{sid}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True
