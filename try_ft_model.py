import os
from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")
client = OpenAI( API_KEY) 

FT_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:toyota-advisor:CZqU0cTY"  

user_question = ""

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    
    data = request.get_json()
    text = data.get("text", "")

  
    user_question = text

    response = client.responses.create(
    model=FT_MODEL,
    input=[
        {
            "role": "user",
            "content": user_question
        }
    ]
)
    return jsonify({"processed": response.output[0].content[0].text})

if __name__ == "__main__":
  
    app.run(host="127.0.0.1", port=5000, debug=True)


