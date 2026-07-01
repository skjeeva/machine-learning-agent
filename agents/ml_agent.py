import re

class MLAgent:

    def explain(self, query):
        query_lower = query.lower()

        from agents.topic_detector import detect_topic
        topic = detect_topic(query_lower)

        if not topic:
            return {
                "topic": None,
                "explanation": "I didn't catch that. Try asking about gradient descent, linear regression, kmeans or decision tree."
            }

        explanation = self._build_explanation(topic, query_lower)

        return {
            "topic": topic,
            "explanation": explanation
        }

    def _build_explanation(self, topic, query):

        simple = any(w in query for w in ["simple", "easy", "eli5", "basics", "beginner", "what is", "explain"])

        explanations = {
            "gradient descent": {
                "simple": "Imagine you're blindfolded on a hilly landscape. You feel the ground under your feet and always take a small step downhill. Eventually you reach the lowest point. That's gradient descent — finding the minimum loss step by step.",
                "default": "Gradient descent is an optimization algorithm. It computes the gradient of the loss function and moves the parameters in the opposite direction. Each step size is controlled by the learning rate. Watch the ball roll into the valley in the animation."
            },
            "linear regression": {
                "simple": "Imagine drawing the best straight line through a cloud of dots. You keep adjusting the line until it's as close as possible to all the dots. That line lets you predict new values. Watch the plane fit the data in the animation.",
                "default": "Linear regression finds the best-fit plane through data by minimizing the sum of squared errors between predictions and actual values. With two features it fits a 3D plane. Watch it rotate into position in the animation."
            },
            "kmeans": {
                "simple": "Imagine grouping people in a room with no labels. You randomly pick 3 leaders. Everyone joins their nearest leader. Leaders move to the center of their group. Repeat until nobody moves. That's K-Means.",
                "default": "K-Means is an unsupervised clustering algorithm. It initializes K centroids randomly, assigns each point to the nearest centroid, then recomputes centroids as cluster means. It repeats until convergence. Watch the centroids fly to their final positions in 3D."
            },
            "decision tree": {
                "simple": "Imagine asking yes/no questions to guess something. Is it cloudy? Is humidity high? Each question splits your data into groups. Keep asking until you reach a final answer. That's a decision tree.",
                "default": "A decision tree partitions the feature space using recursive binary splits. Each internal node tests a feature threshold. Leaves hold the predicted class. The 3D boundary below shows exactly where the splits happen across two features."
            }
        }

        level = "simple" if simple else "default"
        return explanations[topic][level]