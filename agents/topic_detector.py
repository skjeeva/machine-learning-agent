import re

TOPIC_PATTERNS = {
    "gradient descent": [
        "gradient", "descent", "rolling", "ball", "slope", "downhill",
        "minimize", "loss", "learning rate", "step", "valley", "bowl"
    ],
    "linear regression": [
        "linear", "regression", "line", "predict", "price", "house",
        "fit", "slope", "relationship", "continuous", "plane"
    ],
    "kmeans": [
        "kmeans", "k-means", "cluster", "group", "centroid",
        "segment", "partition", "classify", "unsupervised"
    ],
    "decision tree": [
        "decision", "tree", "split", "branch", "leaf", "yes no",
        "questions", "classify", "rain", "if else", "rule"
    ]
}

def detect_topic(query):
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query) 
    words = query.split()

    scores = {}
    for topic, keywords in TOPIC_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in query)
        if score > 0:
            scores[topic] = score

    if not scores:
        return None

    return max(scores, key=scores.get)