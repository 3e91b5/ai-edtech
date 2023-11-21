from openai import OpenAI

# migration guide: https://github.com/openai/openai-python/discussions/742

api_key = ''
def save_apikey(apikey):
    global api_key
    api_key = apikey

def run_gpt(query):
    #TODO
    pass


# TODO: gpt now has error. idk why
def run_gpt_helloworld():
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
	)
    completion = client.completions.create(model='curie', prompt="This is a test")
    print(completion.choices[0].text)
    print(dict(completion).choices[0].text)
    print(completion.model_dump_json(indent=2))
    
# get the question from student and do prompt enginnering for gpt
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
	

