from flask import Flask, request, jsonify, send_file
import requests
import os
from io import BytesIO

app = Flask(__name__)

# API Keys (store securely in production)
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"
HF_API_KEY = "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"

# Chat with Groq and DuckDuckGo fallback
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

def duckduckgo_search(query):
    r = requests.get(f"https://lite.duckduckgo.com/lite/?q={query}")
    if '<a rel="nofollow" class="result-link"' in r.text:
        start = r.text.find('<a rel="nofollow" class="result-link"')
        snippet = r.text[start:start+500]
        return snippet.replace('\n', ' ')
    return "No relevant info found on DuckDuckGo."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    history = data.get("history", [])
    response = chat_with_groq(message, history)
    if "I don't know" in response or "I'm not sure" in response:
        fallback = duckduckgo_search(message)
        response += f"\n\n[DuckDuckGo]: {fallback}"
    return jsonify({"reply": response})

# Image Generation (Stable Diffusion 2)
@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt")
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        headers=headers, json={"inputs": prompt}
    )
    if response.status_code == 200:
        return send_file(BytesIO(response.content), mimetype='image/png')
    return "Image generation failed", 500

# Video Generation (Text-to-Video Zeroscope or DAMO)
@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.json
    prompt = data.get("prompt")
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(
        "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b",
        headers=headers, json={"inputs": prompt}
    )
    if response.status_code == 200:
        return send_file(BytesIO(response.content), mimetype='video/mp4')
    return "Video generation failed", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
