from tools.visualizer import show_gradient_descent_path
from tools.visualizer import show_gradient_descent


def teach():

    print("\n===== GRADIENT DESCENT =====\n")

    print("""
Imagine you're standing on a hill blindfolded.

You can only feel the slope under your feet.

You keep taking small steps downhill.

Eventually you'll reach the lowest point.

That's exactly how Gradient Descent works.
""")

    show_gradient_descent_path()

    print("\nQuiz:")
    print("Why do we move opposite to the gradient?")