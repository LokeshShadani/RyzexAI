from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# GROQ API Setup
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"

@app.route("/")
def index():
    return "✅ Groq Chatbot is running!"

# Call Groq for response
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
    return "Sorry, I couldn't connect to Groq."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    history = data.get("history", [])
    response = chat_with_groq(message, history)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
