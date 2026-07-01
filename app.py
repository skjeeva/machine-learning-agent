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
    result = agent.explain(query)
    return jsonify({
        "topic":result["topic"],
        "explanation":result["explanation"]
    })
if __name__ == "__main__":
    app.run(debug=True)