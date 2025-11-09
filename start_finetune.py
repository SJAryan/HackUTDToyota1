from openai import OpenAI

client = OpenAI( api_key = "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" ) 


TRAIN_FILE_ID = "file-ENdiPLB7DQoFhmtUu382ba"



BASE_MODEL = "gpt-4o-mini-2024-07-18" 

response = client.fine_tuning.jobs.create(
    model=BASE_MODEL,
    training_file=TRAIN_FILE_ID,
    suffix="toyota-advisor",        
)

print("Fine-tune job id:", response.id)
print("Status:", response.status)