from openai import OpenAI
from flask import Flask, request, jsonify

client = OpenAI( api_key = "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" ) 

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


