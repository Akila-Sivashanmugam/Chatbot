from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Load intents JSON data
with open("intents.json") as f:
    intents = json.load(f)["intents"]

# Find matching tag by pattern
def get_response(user_input):
    user_input = user_input.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input:
                return random.choice(intent["responses"])
    # Default fallback if no match
    for intent in intents:
        if intent["tag"] == "no-response":
            return random.choice(intent["responses"])
    return "I'm here to help. Tell me more."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
