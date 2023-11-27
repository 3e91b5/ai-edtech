import os
from dotenv import load_dotenv

load_dotenv()

DBPASSWORD = os.getenv("DBPASSWORD")
GPTPASSWORD = os.getenv("GPTPASSWORD")