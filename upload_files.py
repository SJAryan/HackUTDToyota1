from openai import OpenAI 

client = OpenAI( api_key = "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" ) 


train_file = client.files.create(
    file=open("train.jsonl", "rb"),
    purpose="fine-tune",  # required for fine-tuning files  [oai_citation:4‡OpenAI Platform](https://platform.openai.com/docs/guides/reinforcement-fine-tuning?utm_source=chatgpt.com)
)
print("Training file id:", train_file.id)

