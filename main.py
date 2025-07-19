from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

chat_history = []

# Replace with your real Groq API key (keep it secret!)


@app.route("/")
def index():
    return send_file("index.html")  # Make sure index.html is in the same directory

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
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": chat_history,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
