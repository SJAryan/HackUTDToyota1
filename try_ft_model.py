import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS  
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()
client = OpenAI()

# The specific fine-tuned model you are using
FT_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:toyota-advisor:CZqU0cTY"

# A clean, de-duplicated list of the car models from your original prompt
CAR_LIST = (
    "4Runner, 4Runner i-FORCE MAX, bZ, Camry, Corolla, Corolla Cross, "
    "Corolla Cross Hybrid, Corolla Hatchback, Corolla Hybrid, GR Corolla, "
    "GR Supra, GR86, Grand Highlander, Grand Highlander Hybrid, Highlander, "
    "Highlander Hybrid, Land Cruiser, Mirai, Prius, Prius Plug-in Hybrid, "
    "RAV4, RAV4 Hybrid, RAV4 Plug-in Hybrid, Sequoia, Sienna, Tacoma, "
    "Tacoma i-FORCE MAX, Toyota Crown, Toyota Crown Signia, Tundra, "
    "Tundra i-FORCE MAX"
)

# This is the system prompt. It tells the AI its job and rules.
# We use an f-string to inject the clean car list.
SYSTEM_PROMPT = (
    f"You are an online assistant that will help users find which one of "
    f"these and only these cars will fit their needs: {CAR_LIST}. "
    "The response should just be the names of models in this format: "
    "model1, model2, model3. The models should be organized from the "
    "best fitting option first."
)

app = Flask(__name__)
CORS(app) 

@app.route("/process", methods=["POST"])
def process():
    """
    Handles the POST request, sends the user's text to the OpenAI API,
    and returns the model's recommendation.
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No 'text' field provided"}), 400
            
        text = data.get("text", "")

        # Call the OpenAI API with the correct message structure
        response = client.chat.completions.create(
            model=FT_MODEL,
            messages=[  
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    # We pass the user's raw query here
                    "content": "the needs/wants/users question is " + text
                }
            ],
            temperature=0.0 # Set temperature to 0 for deterministic, factual output
        )
        
        processed_text = response.choices[0].message.content
        
        return jsonify({"processed": processed_text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == "__main__":
    # Note: debug=True is great for development, but should be set to False
    # for a production environment.
    app.run(host="127.0.0.1", port=5000, debug=True)