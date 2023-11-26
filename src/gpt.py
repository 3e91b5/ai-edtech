from openai import OpenAI
import streamlit as st
import datetime

# migration guide: https://github.com/openai/openai-python/discussions/742


def set_apikey(apikey):

    st.session_state["api_key"] = apikey
    # api_key = apikey

def get_apikey():
    return st.session_state["api_key"]


# 0 git branch jwhong
# 1 git add .
# 2 git commit -> commit 메세지 작성
# 3 git push origin jwhong
# origin = 내 로컬 작업환경


def run_gpt(query):
    #TODO
    pass


# TODO: gpt now has an error. idk why. error message below.
def run_gpt_helloworld():
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=get_apikey(),
	)
    completion = client.completions.create(model='gpt-3.5-turbo', prompt="This is a test")
    
    
    
    # print(datetime.datetime.now(), completion.choices[0].text)
    # print(datetime.datetime.now(), dict(completion).choices[0].text)
    # print(datetime.datetime.now(), completion.model_dump_json(indent=2))
    
###### error message ######
# Traceback (most recent call last):
#   File "/home/jhkim/ai-edutech/chatgpt_test.py", line 34, in <module>
#     run_gpt_helloworld()
#   File "/home/jhkim/ai-edutech/chatgpt_test.py", line 16, in run_gpt_helloworld
#     completion = client.chat.completions.create(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_utils/_utils.py", line 299, in wrapper
#     return func(*args, **kwargs)
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/resources/chat/completions.py", line 598, in create
#     return self._post(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 1055, in post
#     return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 834, in request
#     return self._request(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 865, in _request
#     return self._retry_request(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 925, in _retry_request
#     return self._request(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 865, in _request
#     return self._retry_request(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 925, in _retry_request
#     return self._request(
#   File "/home/jhkim/.local/lib/python3.10/site-packages/openai/_base_client.py", line 877, in _request
#     raise self._make_status_error_from_response(err.response) from None
# openai.RateLimitError: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
############################

# get the question from student and do prompt engineering for gpt
def prompt(question):
    #TODO
	pass	





# def gpt_connection():
# 	api_key = '[AUTH_KEY 입력]'
# 	return api_key

# def run_gpt(query):
# 	openai.api_key = gpt_connection()
# 	messages = [{"role": "", "content": ""}] 
# 	response = openai.ChatCompletion.create(
# 		model = 'gpt-4',
# 		messages = messages
# 	)
# 	msg = response['choices'][0]['message']['content']
# 	return msg
	

