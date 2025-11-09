import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

client = OpenAI()

JOB_ID = "ftjob-BiGTKpDyLLUphQ7cwsNhZhV6" 

while True:
    job = client.fine_tuning.jobs.retrieve(JOB_ID)
    print("Status:", job.status, "| trained_tokens:", job.trained_tokens)

    if job.status in ("succeeded", "failed", "cancelled"):
        break

    time.sleep(20)

print("Final status:", job.status)
print("Fine-tuned model id:", job.fine_tuned_model)