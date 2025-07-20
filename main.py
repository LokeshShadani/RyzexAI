from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests, base64, os

app = Flask(__name__)
CORS(app)

GROQ_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HF_KEY = "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"
HF_IMG_MODEL = "stabilityai/stable-diffusion-2"
ZEROSCOPE_URL = "https://hf.space/embed/fffiloni/zeroscope/+/api/predict"

chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    chat_history.append({"role": "user", "content": msg})

    payload = {"model":"llama3-70b-8192", "messages":chat_history, "temperature":0.7}
    headers = {"Authorization": f"Bearer {GROQ_KEY}"}
    r = requests.post(GROQ_URL, headers=headers, json=payload)
    reply = r.json()['choices'][0]['message']['content']
    chat_history.append({"role":"assistant","content":reply})
    return jsonify({"reply": reply})

@app.route("/generate-image", methods=["POST"])
def gen_img():
    prompt = request.json.get("prompt","")
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    r = requests.post(f"https://api-inference.huggingface.co/models/{HF_IMG_MODEL}",
                      headers=headers, json={"inputs": prompt})
    if r.status_code == 200:
        img = base64.b64encode(r.content).decode()
        return jsonify({"image": f"data:image/png;base64,{img}"})
    return jsonify({"error":"Image generation failed"}),500

@app.route("/upload/image", methods=["POST"])
def upload_image():
    f = request.files.get("image")
    if not f: return jsonify({"error":"No file"}),400
    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", f.filename)
    f.save(path)
    return jsonify({"message": f.image uploaded: {f.filename}"})

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text","")
    return jsonify({"say": text})

@app.route("/generate-video", methods=["POST"])
def gen_video():
    prompt = request.json.get("prompt","")
    data = {"data": [prompt]}
    try:
        resp = requests.post(ZEROSCOPE_URL, json=data, timeout=300)
        out = resp.json()
        if resp.status_code==200 and out.get("data"):
            vid_url = out["data"][0]  # Pode dar video URL
            return jsonify({"video": vid_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Video generation failed"}), 500

@app.route("/")
def home():
    return send_file("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
