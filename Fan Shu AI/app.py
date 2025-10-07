from flask import Flask, render_template, request, jsonify # type: ignore
import requests # type: ignore
import os

app = Flask(__name__)

# Get your Hugging Face key from environment variable
HF_API_KEY = os.getenv("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")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_message}

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/gemma-2b-it",
            headers=headers,
            json=payload,
            timeout=20
        )
        result = response.json()

        # Extract generated text safely
        if isinstance(result, list) and "generated_text" in result[0]:
            reply = result[0]["generated_text"]
        else:
            reply = "Sorry, I couldn't understand that."

    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

