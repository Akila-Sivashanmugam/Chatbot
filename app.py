from flask import Flask, render_template, request, jsonify
import json
import random
from difflib import SequenceMatcher

app = Flask(__name__)

# Load counselor data
with open("counsel_chat_250-tokens_full.json") as f:
    data = json.load(f)

# Flatten conversation data
conversations = []
for item in data["train"]:
    for utterance in item["utterances"]:
        question = utterance["history"][0]
        responses = utterance["candidates"]
        conversations.append((question, responses))

# Find the most similar user query
def get_best_response(user_input):
    max_ratio = 0
    best_responses = ["I'm here to listen. Could you tell me more?"]

    for question, responses in conversations:
        ratio = SequenceMatcher(None, user_input.lower(), question.lower()).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            best_responses = responses

    return random.choice(best_responses)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    response = get_best_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
