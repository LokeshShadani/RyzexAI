from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import base64
import os
import speech_recognition as sr
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Create upload folders
if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("audio"):
    os.makedirs("audio")

chat_history = []

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    chat_history.append({"role": "user", "content": user_input})

    if "who made you" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
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
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"❌ Network error: {str(e)}"}), 500
    except KeyError:
        return jsonify({"reply": "❌ API Error: Unexpected response format."}), 500

@app.route("/upload-image", methods=["POST"])
def upload_image():
    file = request.files["image"]
    filename = secure_filename(file.filename)
    path = os.path.join("uploads", filename)
    file.save(path)

    with open(path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    content = f"User uploaded an image. Base64 content: {img_base64[:100]}..."
    chat_history.append({"role": "user", "content": content})

    return jsonify({"reply": "📷 Image uploaded and sent to AI!"})

@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    file = request.files["audio"]
    filename = secure_filename(file.filename)
    path = os.path.join("audio", filename)
    file.save(path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        chat_history.append({"role": "user", "content": f"(Voice): {text}"})
        return jsonify({"reply": f"🎙️ Recognized voice input: {text}"})
    except sr.UnknownValueError:
        return jsonify({"reply": "❌ Could not understand audio"})
    except sr.RequestError:
        return jsonify({"reply": "❌ Voice recognition service failed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
