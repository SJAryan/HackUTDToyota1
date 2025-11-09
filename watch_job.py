import time
from openai import OpenAI

client = OpenAI( api_key = "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" ) 

JOB_ID = "ftjob-e34ENUOdHlCQC8tCgMpCW50X" 

while True:
    job = client.fine_tuning.jobs.retrieve(JOB_ID)
    print("Status:", job.status, "| trained_tokens:", job.trained_tokens)

    if job.status in ("succeeded", "failed", "cancelled"):
        break

    time.sleep(20)

print("Final status:", job.status)
print("Fine-tuned model id:", job.fine_tuned_model)