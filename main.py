from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

chat_history = []

@app.route("/")
def index():
    return send_file("index.html")  # Serving directly from root folder

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    chat_history.append({"role": "user", "content": user_input})

    # Custom creator response
    if "who made you" in user_input.lower() or "your creator" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": chat_history,
        "temperature": 0.7,
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
