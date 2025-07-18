from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import base64
import os

app = Flask(__name__)
CORS(app)

chat_history = []

OPENROUTER_API_KEY = "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"

@app.route("/")
def index():
    return send_file("index.html")  # Ensure index.html is in the root folder

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    chat_history.append({"role": "user", "content": user_input})

    if "who made you" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ryzexai.onrender.com",
        "X-Title": "Ryzex AI"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": chat_history,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"❌ Network error: {str(e)}"}), 500
    except KeyError:
        return jsonify({"reply": "❌ API Error: Unexpected response format."}), 500

@app.route("/upload/audio", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No audio file provided"}), 400

    # Save audio file temporarily
    path = "temp_audio.wav"
    file.save(path)

    # Here you can process it with Whisper or other STT library (not shown)
    return jsonify({"message": "Audio received. Add speech-to-text logic here."})

@app.route("/upload/image", methods=["POST"])
def upload_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    # Save or process image if needed
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    return jsonify({"message": f"Image uploaded: {file.filename}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
