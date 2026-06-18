from flask import Flask, render_template, request, jsonify
from agents.topic_detector import detect_topic
from agents.ml_agent import MLAgent

app = Flask(__name__)
agent = MLAgent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    topic = detect_topic(query)

    if topic:
        explanation = agent.explain(topic)
        return jsonify({
            "topic": topic,
            "explanation": explanation
        })
    else:
        return jsonify({
            "topic": None,
            "explanation": "Sorry, I don't know that topic yet. Try asking about gradient descent, linear regression, kmeans or decision tree."
        })