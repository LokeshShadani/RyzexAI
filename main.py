from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

chat_history = []

API_KEY = "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"

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

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": chat_history,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"❌ Network error: {str(e)}"}), 500
    except KeyError:
        return jsonify({"reply": "❌ API Error: Unexpected response format."}), 500

@app.route("/voice", methods=["POST"])
def voice_input():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"reply": "❌ No audio file provided"}), 400

    try:
        # Whisper API (replace this if you want local Whisper use)
        files = {"file": (audio_file.filename, audio_file, audio_file.mimetype)}
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {
            "model": "whisper-1",
            "response_format": "json"
        }
        whisper_url = "https://api.openai.com/v1/audio/transcriptions"

        r = requests.post(whisper_url, headers=headers, files=files, data=data)
        transcript = r.json()["text"]
        return jsonify({"transcript": transcript})
    except Exception as e:
        return jsonify({"reply": f"❌ Voice processing failed: {str(e)}"}), 500

@app.route("/image", methods=["POST"])
def image_upload():
    image = request.files.get("image")
    if not image:
        return jsonify({"reply": "❌ No image uploaded"}), 400

    # This is a placeholder. OpenRouter doesn’t support image input yet.
    return jsonify({"reply": "🖼️ Image received successfully, but this AI cannot process images yet."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
