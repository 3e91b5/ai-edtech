import streamlit as st
import src.db as db

st.write("problem set page")



def recommend_problem(sid):
    
    pass



def get_problem(sid):
    return
    #TODO: after db schema is fixed, implement this function. below is example code.
    status = db.get_student_status(sid)
    level = db.get_student_level(sid)
    score = db.get_student_score(sid)

    problems = db.get_problems(level, score)
    
    # if there is no problem in the database, return False
    if problems.empty:
        return False
    else:
        # random selection from problems set
        from random import sample
        problem = problems.sample()
        return problems
    

