class MLAgent:

    def explain(self, topic):

        topic = topic.lower()

        explanations = {
            "gradient descent": """
                Imagine you're blindfolded on a hilly landscape.
                You can only feel the slope under your feet.
                You keep taking small steps downhill.
                Eventually you reach the lowest point — the minimum loss.
                Watch the ball roll down the curve in the animation.
            """,
            "linear regression": """
                Imagine predicting house prices from size.
                You draw a line through the data points.
                The line adjusts until it fits as closely as possible.
                Watch the line move to fit the data in the animation.
            """,
            "kmeans": """
                Imagine grouping people in a room with no information.
                You randomly pick 3 leaders — called centroids.
                Everyone joins their nearest leader.
                Leaders move to the center of their group.
                Repeat until nobody moves.
                Watch the clusters form in the animation.
            """,
            "decision tree": """
                Imagine asking yes/no questions to predict rain.
                Is it cloudy? Is humidity high?
                Each question splits the data into groups.
                Keep splitting until you reach a final answer.
                Watch the tree build itself in the animation.
            """
        }

        return explanations.get(topic, "Topic not found")