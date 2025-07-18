@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    chat_history.append({"role": "user", "content": user_input})

    # Custom hardcoded reply
    if "who made you" in user_input.lower() or "your creator" in user_input.lower():
        reply = "I was created by Lokesh Shadani 💡"
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    # OpenRouter + Gemma API
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemma-7b-it",  # Or try "google/gemma-2b-it"
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
