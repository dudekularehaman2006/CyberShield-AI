from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.route("/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY or not client:
        return jsonify({"reply": "Server error: GROQ_API_KEY is not configured."}), 500

    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"reply": "Please provide a message."}), 400

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert. Only answer cybersecurity questions. If outside domain, say it's out of scope."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2,
            max_tokens=300
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("Groq error:", type(e).__name__, e)
        return jsonify({"reply": f"Groq error: {e}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)