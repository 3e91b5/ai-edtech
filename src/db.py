import psycopg2
import streamlit as st
import pandas as pd

def init_connection():
    #### WARNING ####
    # database password should be erased before pushing to github
	return psycopg2.connect("host=147.47.200.145 dbname=teamdb3 user=team3 password=eduteam3# port=34543")
	

def run_query(query):
    print('run query:',  query)
    try:
        conn = init_connection()
        df = pd.read_sql(query, conn)
    except psycopg2.Error as e:
        print("DB error: ", e)
        conn.close()
    finally:
        conn.close()
    return df

def run_tx(query):
	print('run tx:',  query)
	try:
		conn = init_connection()
		with conn.cursor() as cur:
			cur.execute(query)
	except psycopg2.Error as e:
		print("DB error: ", e)
		conn.rollback()
		conn.close()
	finally:
		conn.commit()
		conn.close()
	return


def add_user(pid,password):
	query = f"SELECT * FROM edutech.studentdb WHERE pid = '{pid}'"
	result = run_query(query)

	if result.empty:
		print("user data를 추가합니다.", pid, password)
		add_query = f"INSERT INTO edutech.studentdb (pid, password) VALUES('{pid}', '{password}')"
		run_tx(add_query)
		return True
	else:
		return False

def login_user(pid,password):
	query =f"SELECT * FROM edutech.studentdb WHERE pid ='{pid}' AND password = '{password}'"
	result = run_query(query)

	if result.empty:
		return False
	else:
		return True


def view_all_users():
	query = 'SELECT * FROM edutech.studentdb'
	result = run_query(query)
	return result