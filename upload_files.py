import os
from openai import OpenAI 
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")
client = OpenAI( API_KEY) 

train_file = client.files.create(
    file=open("train.jsonl", "rb"),
    purpose="fine-tune",  # required for fine-tuning files  [oai_citation:4‡OpenAI Platform](https://platform.openai.com/docs/guides/reinforcement-fine-tuning?utm_source=chatgpt.com)
)
print("Training file id:", train_file.id)

