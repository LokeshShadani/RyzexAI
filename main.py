from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import requests
import openai

app = Flask(__name__)
CORS(app)

chat_history = []

# Configure Groq API (OpenAI-compatible endpoint)
openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    chat_history.append({"role": "user", "content": user_input})

    if "who made you" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500

@app.route("/upload/audio", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No audio file provided"}), 400

    path = "temp_audio.wav"
    file.save(path)

    return jsonify({"message": "Audio received. Add speech-to-text logic here."})

@app.route("/upload/image", methods=["POST"])
def upload_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    return jsonify({"message": f"Image uploaded: {file.filename}"})

@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        HF_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        headers = {"Accept": "application/json"}

        response = requests.post(HF_URL, headers=headers, json={"inputs": prompt})

        if response.status_code == 200:
            image_data = response.content
            image_path = "generated_image.png"
            with open(image_path, "wb") as f:
                f.write(image_data)
            return send_file(image_path, mimetype="image/png")
        else:
            return jsonify({"error": f"HuggingFace API error: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
