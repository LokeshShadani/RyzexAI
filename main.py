from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from openai import OpenAI

# ✅ Initialize Flask and CORS
app = Flask(__name__)
CORS(app)

# ✅ Chat history memory
chat_history = []

# ✅ Groq Client setup (acts like OpenAI)
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# ✅ Serve frontend
@app.route("/")
def index():
    return send_file("index.html")

# ✅ Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"reply": "⚠️ Empty message received."}), 400

    chat_history.append({"role": "user", "content": user_input})

    # Hardcoded answer for creator
    if "who made you" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=chat_history
        )
        reply = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500

# ✅ Voice/audio upload (you can connect to speech-to-text here)
@app.route("/upload/audio", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No audio file provided"}), 400

    path = "temp_audio.wav"
    file.save(path)

    return jsonify({"message": "Audio received. (Speech-to-text not implemented yet)"})


# ✅ Image upload
@app.route("/upload/image", methods=["POST"])
def upload_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    return jsonify({"message": f"Image uploaded: {file.filename}"})

# ✅ Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
