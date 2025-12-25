from flask import Flask, render_template, request, jsonify
import pickle
import json
import numpy as np
import sys

sys.path.append("src")
from preprocessing import preprocess_text

app = Flask(__name__)

# Load models
model = pickle.load(open("models/model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("models/label_encoder.pkl", "rb"))

# Load intents
with open("data/intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# Helper functions
def predict_intent(text, threshold=0.3):
    text = preprocess_text(text)
    vec = vectorizer.transform([text])
    probs = model.predict_proba(vec)

    max_prob = np.max(probs)
    index = np.argmax(probs)

    if max_prob < threshold:
        return "fallback"

    return label_encoder.inverse_transform([index])[0]


def get_response(intent):
    for item in intents["intents"]:
        if item["tag"] == intent:
            return np.random.choice(item["responses"])

    return "Sorry, I did not understand that."
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    # Rule-based greetings
    if user_msg.lower() in ["hi", "hello", "hey"]:
        return jsonify({"reply": "Hello 👋 How can I help you?"})

    if user_msg.lower() in ["bye", "goodbye"]:
        return jsonify({"reply": "Goodbye 👋 Have a nice day!"})

    intent = predict_intent(user_msg)
    reply = get_response(intent)

    return jsonify({"reply": reply})
if __name__ == "__main__":
    app.run()
