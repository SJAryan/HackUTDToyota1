import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- 1. Import CORS
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
client = OpenAI()

FT_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:toyota-advisor:CZqU0cTY"

app = Flask(__name__)
CORS(app)  # <-- 2. Enable CORS for your entire app

@app.route("/process", methods=["POST"])
def process():
    
    data = request.get_json()
    text = data.get("text", "")

    
    response = client.chat.completions.create(
        model=FT_MODEL,
        messages=[  
            {
                "role": "user",
                "content": text
            }
        ]
    )
    
    # <-- 4. FIX: Use the correct way to get the response text
    processed_text = response.choices[0].message.content
    
    return jsonify({"processed": processed_text})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)