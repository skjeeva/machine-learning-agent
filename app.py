from agents.ml_agent import MLAgent

agent = MLAgent()

topic = input("What ML topic do you want to learn? ")

agent.teach(topic)