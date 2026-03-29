from flask import Flask, render_template, request, jsonify
from google import genai
from datetime import datetime
import time

app = Flask(__name__)

# GenAI client
client = genai.Client(api_key="AIzaSyCaVMGOu61jW7uCL9wrz-BneLTNxGETAN0")

# Conversation history
conversation_history = []

# ✅ Always get real current time
def get_timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Add user message with CURRENT timestamp
    conversation_history.append({
        "role": "user",
        "content": user_message,
        "time": get_timestamp()
    })

    # Build context with time included
    context = "\n".join([
        f"[{msg.get('time', '')}] {msg['role']}: {msg['content']}"
        for msg in conversation_history
    ])

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=context
        )

        bot_message = response.text.strip()

        # Add bot message with CURRENT timestamp
        conversation_history.append({
            "role": "bot",
            "content": bot_message,
            "time": get_timestamp()
        })

        return jsonify({
            "reply": bot_message,
            "time": get_timestamp()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)