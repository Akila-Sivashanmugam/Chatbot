from flask import Flask, render_template, request, jsonify
import json
import random
from difflib import SequenceMatcher  # ✅ Import this

app = Flask(__name__)

# ✅ Load intents from JSON
with open("intents.json") as f:
    intents = json.load(f)["intents"]

# ✅ Your updated get_response function goes here
def get_response(user_input):
    user_input = user_input.lower()
    best_match = None
    highest_ratio = 0

    for intent in intents:
        for pattern in intent["patterns"]:
            ratio = SequenceMatcher(None, pattern.lower(), user_input).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = intent

    if highest_ratio > 0.6 and best_match:
        return random.choice(best_match["responses"])
    
    # fallback response
    for intent in intents:
        if intent["tag"] == "no-response":
            return random.choice(intent["responses"])
    
    return "I'm here to help. Tell me more."

# ✅ Routes for chatbot
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)
