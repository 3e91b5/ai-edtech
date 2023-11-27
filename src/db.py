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

def add_user(sid,password, name, age, grade):
	# query = f"SELECT * FROM edutech.studentdb WHERE sid = '{sid}'"
	query = f"SELECT * FROM student_db.students WHERE account = '{sid}'"
	print(datetime.datetime.now(), "check query:", query)
	result = run_query(query)

	if result.empty:
		print(datetime.datetime.now(), "user data를 추가합니다.", sid, password)
		# add_query = f"INSERT INTO edutech.studentdb (sid, password, admin) VALUES('{sid}', '{password}', False)"
		date_joined = datetime.datetime.now()
		add_query = f"INSERT INTO student_db.students (account, password, admin, name,age, grade,date_joined) VALUES('{sid}', '{password}', False,'{name}', '{age}', '{grade}', '{date_joined}')"

		run_tx(add_query)
		return True
	else:
		return False

def login_user(sid,password):
	# query =f"SELECT * FROM edutech.studentdb WHERE sid ='{sid}' AND password = '{password}'"
	query = f"SELECT * FROM student_db.students WHERE account = '{sid}' AND password = '{password}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		last_login = datetime.datetime.now()
		query = f"UPDATE student_db.students SET last_login = '{last_login}' WHERE account = '{sid}'"
		run_tx(query)
		return True

def view_all_users():
	# query = 'SELECT * FROM edutech.studentdb'
	query = 'SELECT * FROM student_db.students'
	result = run_query(query)
	return result

def delete_user(sid):
	query = f"select * from student_db.students where account = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	query = f"DELETE FROM student_db.students WHERE account = '{sid}'"
	run_tx(query)
	print(datetime.datetime.now(), "delete user", sid)
	
	return True

def is_admin(sid):
	# query = f"SELECT admin FROM edutech.studentdb WHERE sid = '{sid}'"
	query = f"SELECT admin FROM student_db.students WHERE account = '{sid}'"
	result = run_query(query)
	print(datetime.datetime.now(), "is_admin",  result['admin'][0])
	
	if result['admin'][0] == True:
		return True
	else:
		return False

def update_user_password(sid, new_password):
	query = f"UPDATE student_db.students SET password = '{new_password}' WHERE account = '{sid}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True
	
def update_student_score(sid, score):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.		
	query = f"UPDATE edutech.studentdb SET score = '{score}' WHERE sid = '{sid}'"
	result = run_tx(query)
	if result.empty:
		return False
	else:
		return True

def get_student_score(sid):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.
	query = f"SELECT score FROM edutech.studentdb WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

def get_student_status(sid):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.
	query = f"SELECT status FROM edutech.studentdb WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

def get_student_level(sid):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.
	query = f"SELECT level FROM edutech.studentdb WHERE sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# given the level of student and the score vector from student's answer, get a few problems from database
def get_problems_recommendation(level, score):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.
	query = f"SELECT * FROM edutech.problems WHERE level = '{level}' AND score = '{score}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

# given the level of student and the score vector from student's answer, get one problem from database
def get_problem_recommendation(level, score, sid):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.
	query = f"SELECT * FROM edutech.problems WHERE level = '{level}' AND score = '{score}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result

#
def get_problem(pid):
	return
	#TODO: after db schema is fixed, implement this function. below is example code.
	query = f"SELECT * FROM edutech.problems WHERE pid = '{pid}'"
	result = run_query(query)
	if result.empty:
		return False
	else:
		return result