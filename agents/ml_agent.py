class MLAgent:

    def teach(self, topic):

        topic = topic.lower()

        if topic == "gradient descent":
            from topics.gradient_descent import teach
            teach()

        elif topic == "linear regression":
            from topics.linear_regression import teach
            teach()

        elif topic == "kmeans":
            from topics.kmeans import teach
            teach()

        elif topic == "decision tree":
            from topics.decision_tree import teach
            teach()

        else:
            print("Topic not found")