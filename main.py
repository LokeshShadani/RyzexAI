# main.py
from flask import Flask, request, jsonify, send_file
import requests
import base64
from io import BytesIO

app = Flask(__name__)

# Groq API
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Hugging Face Image Generation API
HF_API_KEY = "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"
HF_MODEL = "stabilityai/stable-diffusion-2"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are Ryzex, a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    data = response.json()
    reply = data['choices'][0]['message']['content']
    return jsonify({"reply": reply})


@app.route("/generate-image", methods=["POST"])
def generate_image():
    prompt = request.json.get("prompt", "")

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers, json=payload
    )

    if response.status_code == 200:
        img_data = base64.b64encode(response.content).decode("utf-8")
        return jsonify({"image": f"data:image/png;base64,{img_data}"})
    else:
        return jsonify({"error": "Image generation failed."}), 500


@app.route("/")
def index():
    return send_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)
