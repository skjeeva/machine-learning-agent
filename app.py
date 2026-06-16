from agents.ml_agent import MLAgent
from agents.topic_detector import detect_topic

agent = MLAgent()

query = input("Ask me about ML: ")

topic = detect_topic(query)

if topic:
    agent.teach(topic)
else:
    print("Sorry, I don't know that topic yet.")