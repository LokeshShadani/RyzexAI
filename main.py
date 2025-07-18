from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

chat_history = []

@app.route("/")
def index():
    return send_file("index.html")  # Ensure this file exists

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    chat_history.append({"role": "user", "content": user_input})

    # Hardcoded response
    if "who made you" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
