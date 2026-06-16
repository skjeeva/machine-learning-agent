from tools.visualizer import show_linear_regression, show_linear_regression_3d

def teach():

    print("\n===== LINEAR REGRESSION =====\n")

    print("""
Imagine you're trying to predict house prices based on size.

You have a bunch of data points — each one is a house with a size and a price.

You want to draw the best straight line through all those points.

Linear Regression finds that line by minimizing the error between
the line's predictions and the actual prices.
""")

    show_linear_regression()

    print("""
Now imagine you have TWO features — house size AND number of rooms.

Instead of a line, you now fit a PLANE through 3D space.

Same idea, one more dimension.
""")

    show_linear_regression_3d()

    print("\nQuiz:")
    print("What does linear regression minimize to find the best line?")