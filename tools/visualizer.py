import numpy as np
import plotly.graph_objects as go


def show_gradient_descent():

    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)

    X, Y = np.meshgrid(x, y)

    Z = X**2 + Y**2

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z
            )
        ]
    )

    fig.show()