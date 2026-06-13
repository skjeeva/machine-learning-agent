import numpy as np
import plotly.graph_objects as go

def loss(x, y):
    return x**2 + y**2

x = 4
y = 4

learning_rate = 0.1

path_x = []
path_y = []
path_z = []

for _ in range(20):

    z = loss(x, y)

    path_x.append(x)
    path_y.append(y)
    path_z.append(z)

    dx = 2 * x
    dy = 2 * y

    x = x - learning_rate * dx
    y = y - learning_rate * dy

grid = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(grid, grid)
Z = X**2 + Y**2

fig = go.Figure()

fig.add_trace(
    go.Surface(
        x=X,
        y=Y,
        z=Z,
        opacity=0.8
    )
)

fig.add_trace(
    go.Scatter3d(
        x=path_x,
        y=path_y,
        z=path_z,
        mode='lines+markers',
        marker=dict(size=5),
        line=dict(width=6),
        name='Gradient Descent Path'
    )
)

fig.show()