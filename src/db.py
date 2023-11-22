import psycopg2
import streamlit as st
import pandas as pd
import datetime

def init_connection():
    #### WARNING ####
    # database password should be erased before pushing to github
	return psycopg2.connect("host=147.47.200.145 dbname=teamdb3 user=team3 password=eduteam3# port=34543")
	

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
	query = f"SELECT * FROM edutech.studentdb WHERE sid = '{sid}'"
	result = run_query(query)

	if result.empty:
		print(datetime.datetime.now(), "user data를 추가합니다.", sid, password)
		add_query = f"INSERT INTO edutech.studentdb (sid, password, admin) VALUES('{sid}', '{password}', False)"
		run_tx(add_query)
		return True
	else:
		return False

def login_user(sid,password):
	query =f"SELECT * FROM edutech.studentdb WHERE sid ='{sid}' AND password = '{password}'"
	result = run_query(query)

	if result.empty:
		return False
	else:
		return True

def view_all_users():
	query = 'SELECT * FROM edutech.studentdb'
	result = run_query(query)
	return result

def delete_user(sid):
	query = f"select * from edutech.studentdb where sid = '{sid}'"
	result = run_query(query)
	if result.empty:
		return False
	query = f"DELETE FROM edutech.studentdb WHERE sid = '{sid}'"
	run_tx(query)
	print(datetime.datetime.now(), "delete user", sid)
	
	return True

def is_admin(sid):
	query = f"SELECT admin FROM edutech.studentdb WHERE sid = '{sid}'"
	result = run_query(query)
	if result == True:
		return True
	else:
		return False


def update_user_password(sid, new_password):
	query = f"UPDATE edutech.studentdb SET password = '{new_password}' WHERE sid = '{sid}'"
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