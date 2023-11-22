from openai import OpenAI
import time
import datetime

apikey = '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'




# TODO: gpt now has error. idk why. error message below.
def run_gpt_helloworld():
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=apikey,
	)
    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )

    print(datetime.datetime.now(), completion.choices[0].message)
    
    
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



# run_gpt_helloworld()
import random
randomlist = random.sample(range(10, 30), 5)
print(randomlist)