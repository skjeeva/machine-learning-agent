def detect_topic(user_input):

    text = user_input.lower()

    if "gradient" in text:
        return "gradient descent"

    elif "regression" in text:
        return "linear regression"

    elif "kmeans" in text or "k-means" in text:
        return "kmeans"

    elif "decision tree" in text:
        return "decision tree"

    return None