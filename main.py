from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

chat_history = []

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
        # Use Puter SDK on frontend; simulate response backend-side if needed
        reply = "🧠 Ask me anything! (Response should come from Puter API via frontend JS)"
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
