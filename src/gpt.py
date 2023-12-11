import requests
from openai import OpenAI
import streamlit as st
import datetime
import src.db as db
import base64
from src.langchain import langchain_single_chat
import requests
from langchain.prompts import PromptTemplate
import psycopg2
from langchain.chat_models import ChatOpenAI

def set_apikey(apikey):

    st.session_state["api_key"] = apikey

def get_apikey():
    return st.session_state["api_key"]


# run run_gpt_helloworld() when the user first submit gpt api key
def run_gpt_helloworld():
    client = OpenAI(
    api_key=get_apikey(),
	)
    messages = [
        {'role':"assistant", 'content':"You are professional mathematics teacher. As a good and kind teacher, you are teaching a student who is struggling with math. The student is asking you a question. Please answer the question."},
        {"role": "user", "content": f"Hello. I am {st.session_state['account']}! Please answer using 1 sentence include my name."}, # this prompt should be improved
    ]
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    response = completion.choices[0].message.content
    
    return response,  client # TODO: return client can maintain the chat session and remember the context?
    
# get the question from student and do prompt engineering for gpt
def default_prompt():
    messages = [
        {'role':"assistant", 'content':"You are professional mathematics teacher. As a good and kind teacher, you are teaching a student who is struggling with math. The student is asking you a question. Please answer the question."},
    ]
    return messages

# prompting for student's 1 time question
def prompt_question(question):
    # TODO
    messages = [{}]
    return messages

# prompting for student's interactive communication
def prompt_communication(question):
    # TODO
    messages = [{}]
    return messages


# using prompted messages, run gpt and get the response
def run_gpt(messages, client):
    completion = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    response = completion.choices[0].message.content
    return response

# function for sending handwritten message and get latex to gpt-4-vision model
def run_gpt_handwritten(url):
    client = OpenAI(
    api_key=get_apikey(),
	)
    completion = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user", 
        "content": [
            {"type": "text", "text": "This is a handwritten answer to a math problem. Encode it into LATEX."},
            {
                "type": "image_url",
                "image_url": {
                "url": url,
                },
            }
        ],
        }
    ],
    )
    return completion.choices[0].message.content

def scored(answer):
    # input은 latex 답안
    # db에 채점 결과 넣는 것 까지. return 따로 없음.
    # db.update_solved(problem_id, student_id, score, ocr_solved)
    return True



knowledge_str = db.init_knowledge_str()
# TEMPLATES: knowledge_map_db.problem

templates = {}
example = {"step 1": "text", "step 2": "text"}

templates["high_school"] = """
You are a high school mathematics instructor. You need to evaluate if every mathematical question in the given dataset is relevant to a topic covered in high school math courses.
Following is one example of the given data:
Problem: "We roll a fair 6-sided die 5 times. What is the probability that we get a 6 in at most 2 of the rolls?"
Level: "Level 5"
Type: "Counting & Probability"
Solution: (solution to the math problem)

Evaluate the Type feature in the given dataset. If Type is either Intermediate Algebra or Precalculus, answer 1. If not, answer 0.
Your responses should consist of either 1 or 0, with no other comments, explanations, reasoning, or dialogue.
"""

# templates["post_process"] = """
# You are a high school mathematics instructor. We will be processing data from the MATH dataset.

# Following is one example of the given data:
# Problem: "We roll a fair 6-sided die 5 times. What is the probability that we get a 6 in at most 2 of the rolls?"
# Level: "Level 5"
# Type: "Counting & Probability"
# Solution: (solution to the math problem)

# First, evaluate the Problem feature in the given dataset.

# Then, identify 1 to 3 math topic(s) within {knowledge_str}, in which knowledge_name refers to math topics covered in Korean high school math courses, that are *relevant* to the math problem.
# A *relevant* math topic covers mathematical rules, concepts, conditions, or assumptions that must applied to solving the math problem.

# Finally, return answer in JSON format (do not include any other comments, explanations, reasoning, or dialogue):
# question: text -> translate the Problem feature in the data into Korean (formal style) and encapsulate LaTeX expressions with $
# solution: json -> in Korean (formal style), create a step-by-step solution to the math question. Encapsulate LaTeX expressions with $. An example would be {example}
# hint: text -> in one to two sentences, provide a hint in Korean on how to approach and solve the problem
# level: int -> extract the number within the Level feature in the data
# knowledge_score: json -> key: each relevant math topic (knowledge_name) extracted from {knowledge_str}, value: total number of rules, mathematical concepts, conditions, or assumptions covered in the topic, which must be applied to solve the math problem
# """.format(example=example, knowledge_str=knowledge_str)

templates["insert_problem"] = """
You are a text-to-SQL translator that writes PostgreSQL code based on plain-language prompts.
- Language: PostgreSQL
- Table: knowledge_map_db.problem, columns = [question text, solution text, hint text, level int, knowledge_score json]

Return nothing but a ready-to-execute and syntactically-correct PostgreSQL query. Output only plain text. Do not output markdown.
Format of desired output is as follows:
INSERT INTO knowledge_map_db.problem (question, solution, hint, level, knowledge_score)
VALUES (
  '다음 방정식 \\[2x^2 + y^2 + 8x - 10y + c = 0\\]의 그래프가 단일 점으로 이루어져 있다고 가정합니다.',
  '{"step_1": "주어진 방정식을 타원의 표준형으로 재작성하려고 시도합니다. 두 변수에 대해 제곱을 완성하면 다음과 같습니다.", "step_2": "\\[\\begin{aligned} 2(x^2+4x) + (y^2-10y) + c &= 0 \\\\ 2(x^2+4x+4) + (y^2-10y+25) + c &= 33 \\\\ 2(x+2)^2 + (y-5)^2 &= 33-c."}',
  '방정식을 타원의 표준형으로 변형시키고, 퇴화된 타원이 되려면 어떤 조건이 필요한지 생각해보세요.',
  3,
  '{"68": 1, "77": 1, "78": 1}'
);

"""

# TEMPLATES: student_db.problem_progress

graded_result = {}

knowledge_str = db.init_knowledge_str()
graded_result["knowledge_score"] = """
You are a high school mathematics instructor who needs to grade the given answer to a math question.

Below is a high-school math problem and solution. 

1. problem: {question}

2. solution: {solution}


In {knowledge}, key indicates math topics covered in Korean high school math courses that are *relevant* to this math problem. value indicates the number of rules, mathematical concepts, conditions, and assumptions that must be applied to solve this math question.
A *relevant* math topic covers mathematical rules, concepts, conditions, or assumptions that must applied to solving the math problem.

Then, identify rules, mathematical concepts, conditions, or assumptions covered in each math topic that must be applied to solve the math problem
Finally, for each rule, concept, condition, or assumption, assign a score to the handwritten answer according to the following criteria:
0 if not applied in the given answer
0.5 if applied incorrectly in the given answer
1 if applied correctly in the given answer

Format your response as a comma separated list with values indicating the total score for each topic. Length of the list MUST match the number of *relevant* math topics for this question.
Examples:
    If number of relevant math topics is three, desired output is as follows: [1, 2.5, 0]
    If number of relevant math topics is six, desired output is as follows: [1, 2.5, 0, 0.5, 1, 1]

Your responses should consist of desired output format with no other comments, explanations, reasoning, or dialogue.
"""

graded_result["feedback"] = """
You are a high school mathematics instructor who needs to grade the given answer to a math question.
To do so, you must compare the given solution with the given answer.

Below is a high-school math problem and solution. 

1. math problem: {question}

2. solution: {solution}

When evaluating the answer, pay attention to whether the student:
- comprehends the problem and considers any assumptions being made
- identifies and applies relevant rules, mathematical concepts, conditions, and assumptions
- executes arithmetic calculations with precision

Format your response as JSON with the following keys.
(1) score (value between 0 and 10): Give extra points for steps that require mathematical reasoning. Assign lower scores for steps that do not require mathematical reasoning skills. Examples include steps that "simplify expressions" or “do arithmetic calculations.”
(2) feedback (text): In Korean, explain why the student gets a certain score. guide the student through his solution step by step, highlighting areas where errors were made.


Your responses should consist of valid JSON syntax, with no other comments, explanations, reasoning, or dialogue not consisting of valid JSON.
Format of desired output is as follows: {{score: 10, feedback: "문제를 잘 이해하고, 적절한 수학적 개념인 산술 기하 평균 부등식을 적용하여 문제를 풀었습니다. 주어진 식 $\\frac{{a}}{{b}} + \\frac{{5b}}{{a}}$에 대해 산술 기하 평균 부등식을 적용한 후, 두 항의 곱이 $5$임을 확인하고, 최소값이 $2\\sqrt{{5}}$임을 정확하게 도출했습니다. 계산도 정확하게 수행되었습니다."}}
"""

graded_result["insert_answer"] = """
You are a text-to-SQL translator that writes PostgreSQL code based on plain-language prompts.
- Language: PostgreSQL
- Table: student_db.problem_progress, columns = [student_id int4, problem_id int4, student_answer text, knowledge_score _int4, score float8, correctness int4, feedback text]

Return nothing but a ready-to-execute and syntactically-correct PostgreSQL query. Output only plain text. Do not output markdown.
Example Format of desired output is as follows:
INSERT INTO student_db.problem_progress (student_id, problem_id, student_answer, knowledge_score, score, correctness, feedback, timestamp)
VALUES (12345678, 
  1,
  {"step 1": "$a$와 $b$가 양의 실수이므로, 산술평균-기하평균 부등식(AM-GM 부등식)을 적용할 수 있습니다.", "step 2": "AM-GM 부등식에 의해 $\frac{a}{b} + \frac{5b}{a} \geq 2\sqrt{\frac{a}{b} \cdot \frac{5b}{a}} = 2\sqrt{5}$입니다.", "step 3": "등호가 성립하는 경우는 $\frac{a}{b} = \frac{5b}{a}$일 때이므로, $a^2 = 5b^2$입니다.", "step 4": "따라서 최솟값은 $2\sqrt{5}$입니다."},
  {1,1},
  4.0,
  0,
  '최종 답은 틀렸으나 문제를 잘 이해하고, 적절한 수학적 개념을 적용하여 문제를 풀었습니다.',
  '2023-12-01'
);

"""





def answer_to_latex(problem, uploaded_file):
    # encode image to base64
    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')

    api_key = st.secrets['apikey']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": f"""

                In the url is a handwritten answer to a high-school level math problem.
                Transcribe the handwritten answer, which is written in Korean, to text. 
                Your response will be used to display mathematical equations on a website using the Streamlit library in Python.
                Format your response appropriately with line breaks (two whitespace followed by double backslash) according to the screen size.
                screen size: -------------------------------------------------------------------------------------------------------------------

                Do NOT wrap mathematical notations with dollar signs or square brackets. Notate whitespace as \quad.
                Double check your response; Make sure ALL text and mathematical notations in the image are included. Do not paraphrase.

                Below is a high-school math problem and solution. 

                1. math problem: {problem["question"]}

                2. solution: {problem["solution"]}
                """
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 3000 # prompt가 이미 거의 token 2000개라, max_token 안 늘리면 답변 이상함!
    }

    # print(payload)

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response.json())
    # 'content' 부분만 추출하여 출력
    content = response.json()['choices'][0]['message']['content']

    return content

def grade_answer(student_id, problem_id, image):
    # Initialize chat models
    gpt_4 = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.3, api_key=st.secrets['apikey'])
    gpt_3 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, api_key=st.secrets['apikey'])

    problem = db.get_selected_problem(problem_id)
    student_answer = answer_to_latex(problem, image) # image_path 변수 정의해야 함

    question = problem["question"]
    solution = problem["solution"]
    knowledge = problem["knowledge_score"]

    template_knowledge = PromptTemplate(
        input_variables=[f"{question}", f"{solution}",f"{knowledge}"],
        template=graded_result["knowledge_score"]
    )
    prompt_knowledge = template_knowledge.format(question = question, solution = solution, knowledge = knowledge)

    template_feedback = PromptTemplate(
        input_variables=[f"{question}", f"{solution}"],
        template=graded_result["feedback"]
    )
    prompt_feedback = template_feedback.format(question = question, solution = solution)

    knowledge_score = langchain_single_chat(gpt_4, prompt_knowledge, f"{student_answer}")
    feedback = langchain_single_chat(gpt_4, prompt_feedback, f"{student_answer}")
    # load date on timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    student_progress = f"student_id: {student_id}, problem_id: {problem_id}, student_answer: {student_answer}, knowledge_score: {knowledge_score}, {feedback}, timestamp: {timestamp}"
    # print("answer_dct: ", student_progress)

    insert_answer_query = langchain_single_chat(gpt_4, graded_result["insert_answer"], f"{student_progress}")
    # print("insert_answer_query: ", insert_answer_query)

    connection = db.init_connection()
    # try:
    cursor = connection.cursor()
    cursor.execute(insert_answer_query)
    # except (Exception, psycopg2.Error) as error:
        # print("Error while connecting to PostgreSQL", error)
        # connection.rollback()
    # finally:
    cursor.close()
    connection.commit()

