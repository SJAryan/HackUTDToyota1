import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")
client = OpenAI( API_KEY) 

JOB_ID = "ftjob-e34ENUOdHlCQC8tCgMpCW50X" 

while True:
    job = client.fine_tuning.jobs.retrieve(JOB_ID)
    print("Status:", job.status, "| trained_tokens:", job.trained_tokens)

    if job.status in ("succeeded", "failed", "cancelled"):
        break

    time.sleep(20)

print("Final status:", job.status)
print("Fine-tuned model id:", job.fine_tuned_model)