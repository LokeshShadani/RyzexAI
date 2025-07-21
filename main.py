from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# API Key & Model for Groq
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"

# Root route for Render check
@app.route("/")
def home():
    return "✅ Ryzex Chatbot backend is running!"

# Function to query Groq
def chat_with_groq(message, history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": history + [{"role": "user", "content": message}]
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()['choices'][0]['message']['content']
    return "❌ Failed to connect to Groq."

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    history = data.get("history", [])
    response = chat_with_groq(message, history)
    return jsonify({"reply": response})

# Render-compatible run block
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
