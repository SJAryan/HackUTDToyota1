import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")
client = OpenAI( API_KEY) 


TRAIN_FILE_ID = "file-ENdiPLB7DQoFhmtUu382ba"



BASE_MODEL = "gpt-4o-mini-2024-07-18" 

response = client.fine_tuning.jobs.create(
    model=BASE_MODEL,
    training_file=TRAIN_FILE_ID,
    suffix="toyota-advisor",        
)

print("Fine-tune job id:", response.id)
print("Status:", response.status)