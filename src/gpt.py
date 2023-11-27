import requests
from openai import OpenAI
import datetime
import os
from dotenv import load_dotenv


# migration guide: https://github.com/openai/openai-python/discussions/742

#### WARNING ####
# api key should be removed before pushing to github
load_dotenv()
GPTPASSWORD = os.getenv("GPTPASSWORD")

def get_ocr(url):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
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
