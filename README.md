# 🤖 Ryzex – AI Chatbot Using Flask & Groq API

This Python-based AI chatbot project utilizes **Flask** for the web server and **Groq's LLaMA 3 API** for generating responses. It features a simple and clean user interface that allows users to interact with the chatbot via text. Voice and image support can also be integrated.

---

## 🧠 Project Overview

The chatbot accepts user input from a frontend interface and responds using Groq's LLaMA 3 model via an API call. It includes persistent conversation history and basic custom response logic.

---

## ✅ Key Features

1. **Flask Backend**  
   Lightweight web server for handling user input and serving the frontend.

2. **Groq API Integration**  
   Uses `llama3-8b-8192` model via Groq’s fast inference API.

3. **Persistent Chat History**  
   Maintains context using a list of messages for realistic conversations.

4. **Custom Responses**  
   Handles hardcoded phrases like `"who made you"` with custom replies.

5. **Cross-Origin Support**  
   Enabled via `flask-cors` to allow frontend-backend communication.

6. **Direct HTML Rendering**  
   Frontend served directly using `send_file("index.html")`, no template folder required.

---

## 💬 How It Works

1. The user sends a message through the web interface.
2. The backend captures it and appends it to `chat_history`.
3. A POST request is made to Groq’s API with the full conversation.
4. The response is parsed and displayed in the chat interface.

---

## 🚀 How to Run

1. Make sure you have **Python 3.8+** installed.
2. Install required libraries:

```bash
pip install flask flask-cors requests
