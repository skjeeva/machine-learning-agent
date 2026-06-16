from tools.visualizer import show_decision_tree

def teach():

    print("\n===== DECISION TREE =====\n")

    print("""
Imagine you're trying to figure out if it will rain today.

You ask a series of yes/no questions:

    Is it cloudy? 
        Yes → Is the humidity high?
            Yes → It will RAIN
            No  → Maybe no rain
        No  → It will NOT rain

That's a Decision Tree — a series of questions that splits
the data into groups until you reach a final answer.

Each split is chosen to separate the data as cleanly as possible.
""")

    show_decision_tree()

    print("\nQuiz:")
    print("What criteria does a Decision Tree use to decide the best split?")