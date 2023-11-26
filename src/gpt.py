import requests
from openai import OpenAI
import datetime

# migration guide: https://github.com/openai/openai-python/discussions/742

api_key = ''    
#### WARNING ####
# api key should be removed before pushing to github

def save_apikey(apikey):
    global api_key
    api_key = apikey

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
