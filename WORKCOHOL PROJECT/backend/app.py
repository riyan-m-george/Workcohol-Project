import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

app = Flask(__name__)
CORS(app)

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Updated client initialization

@app.route("/generate", methods=["POST"])
def generate_story():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = openai_client.chat.completions.create(  # Updated API call
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a story generator."},
                      {"role": "user", "content": prompt}]
        )

        story = response.choices[0].message.content  # Corrected response extraction
        return jsonify({"story": story})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
