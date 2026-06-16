import numpy as np
import plotly.graph_objects as go


import numpy as np
import plotly.graph_objects as go


def show_gradient_descent_path():

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
            mode="lines+markers",
            name="Gradient Descent Path"
        )
    )

    fig.show()



def show_linear_regression_3d():

    np.random.seed(42)
    x1 = np.random.uniform(0, 10, 100)   # house size
    x2 = np.random.uniform(0, 5, 100)    # number of rooms
    y = 2 * x1 + 3 * x2 + 1 + np.random.randn(100) * 2

    # Fit a plane using least squares
    A = np.column_stack([x1, x2, np.ones(100)])
    coeffs, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    m1, m2, b = coeffs

    # Create grid for the plane
    x1_grid = np.linspace(0, 10, 30)
    x2_grid = np.linspace(0, 5, 30)
    X1, X2 = np.meshgrid(x1_grid, x2_grid)
    Y_plane = m1 * X1 + m2 * X2 + b

    fig = go.Figure()

    # Scatter points
    fig.add_trace(go.Scatter3d(
        x=x1,
        y=x2,
        z=y,
        mode="markers",
        name="Data points",
        marker=dict(size=4, color="steelblue")
    ))

    # Best-fit plane
    fig.add_trace(go.Surface(
        x=X1,
        y=X2,
        z=Y_plane,
        opacity=0.6,
        name="Best fit plane",
        colorscale="Reds",
        showscale=False
    ))

    fig.update_layout(
        title="Linear Regression — 3D (two features)",
        scene=dict(
            xaxis_title="House Size",
            yaxis_title="Rooms",
            zaxis_title="Price"
        )
    )

    fig.show()

def show_kmeans():

    np.random.seed(42)

    # Generate 3 natural clusters
    cluster1 = np.random.randn(50, 2) + [2, 2]
    cluster2 = np.random.randn(50, 2) + [8, 8]
    cluster3 = np.random.randn(50, 2) + [2, 8]
    data = np.vstack([cluster1, cluster2, cluster3])

    # Random initial centroids
    centroids = data[np.random.choice(len(data), 3, replace=False)]

    frames = []
    colors_per_frame = []

    for iteration in range(10):

        # Assign each point to nearest centroid
        distances = np.array([
            np.linalg.norm(data - c, axis=1) for c in centroids
        ])
        labels = np.argmin(distances, axis=0)

        colors_per_frame.append(labels.copy())

        # Move centroids to mean of their cluster
        new_centroids = np.array([
            data[labels == k].mean(axis=0) if (labels == k).any() else centroids[k]
            for k in range(3)
        ])
        centroids = new_centroids
        frames.append(centroids.copy())

    # Build animated plotly figure
    color_map = {0: "steelblue", 1: "coral", 2: "mediumseagreen"}

    fig_frames = []

    for i, (centroid_pos, labels) in enumerate(zip(frames, colors_per_frame)):

        point_colors = [color_map[l] for l in labels]

        fig_frames.append(go.Frame(
            data=[
                go.Scatter(
                    x=data[:, 0],
                    y=data[:, 1],
                    mode="markers",
                    marker=dict(color=point_colors, size=7),
                    name="Data points"
                ),
                go.Scatter(
                    x=centroid_pos[:, 0],
                    y=centroid_pos[:, 1],
                    mode="markers",
                    marker=dict(color=["steelblue", "coral", "mediumseagreen"],
                                size=18, symbol="x", line=dict(width=3)),
                    name="Centroids"
                )
            ],
            name=f"Iteration {i+1}"
        ))

    # Initial frame
    initial_colors = [color_map[l] for l in colors_per_frame[0]]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=data[:, 0],
                y=data[:, 1],
                mode="markers",
                marker=dict(color=initial_colors, size=7),
                name="Data points"
            ),
            go.Scatter(
                x=frames[0][:, 0],
                y=frames[0][:, 1],
                mode="markers",
                marker=dict(color=["steelblue", "coral", "mediumseagreen"],
                            size=18, symbol="x", line=dict(width=3)),
                name="Centroids"
            )
        ],
        frames=fig_frames
    )

    fig.update_layout(
        title="K-Means Clustering — watch the centroids move!",
        xaxis_title="Feature 1",
        yaxis_title="Feature 2",
        updatemenus=[dict(
            type="buttons",
            buttons=[
                dict(label="Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 800}, "fromcurrent": True}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"mode": "immediate"}])
            ]
        )],
        sliders=[dict(
            steps=[
                dict(method="animate",
                     args=[[f"Iteration {i+1}"], {"mode": "immediate"}],
                     label=f"Step {i+1}")
                for i in range(10)
            ]
        )]
    )

    fig.show()

def show_kmeans_3d():

    np.random.seed(42)

    # Generate 3 natural clusters in 3D
    cluster1 = np.random.randn(50, 3) + [2, 2, 2]
    cluster2 = np.random.randn(50, 3) + [8, 8, 8]
    cluster3 = np.random.randn(50, 3) + [2, 8, 5]
    data = np.vstack([cluster1, cluster2, cluster3])

    # Random initial centroids
    centroids = data[np.random.choice(len(data), 3, replace=False)]

    frames = []
    colors_per_frame = []

    for iteration in range(10):

        # Assign each point to nearest centroid
        distances = np.array([
            np.linalg.norm(data - c, axis=1) for c in centroids
        ])
        labels = np.argmin(distances, axis=0)
        colors_per_frame.append(labels.copy())

        # Move centroids
        new_centroids = np.array([
            data[labels == k].mean(axis=0) if (labels == k).any() else centroids[k]
            for k in range(3)
        ])
        centroids = new_centroids
        frames.append(centroids.copy())

    color_map = {0: "steelblue", 1: "coral", 2: "mediumseagreen"}
    fig_frames = []

    for i, (centroid_pos, labels) in enumerate(zip(frames, colors_per_frame)):

        point_colors = [color_map[l] for l in labels]

        fig_frames.append(go.Frame(
            data=[
                go.Scatter3d(
                    x=data[:, 0],
                    y=data[:, 1],
                    z=data[:, 2],
                    mode="markers",
                    marker=dict(color=point_colors, size=5),
                    name="Data points"
                ),
                go.Scatter3d(
                    x=centroid_pos[:, 0],
                    y=centroid_pos[:, 1],
                    z=centroid_pos[:, 2],
                    mode="markers",
                    marker=dict(
                        color=["steelblue", "coral", "mediumseagreen"],
                        size=12,
                        symbol="cross",
                        line=dict(width=3)
                    ),
                    name="Centroids"
                )
            ],
            name=f"Iteration {i+1}"
        ))

    initial_colors = [color_map[l] for l in colors_per_frame[0]]

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=data[:, 0],
                y=data[:, 1],
                z=data[:, 2],
                mode="markers",
                marker=dict(color=initial_colors, size=5),
                name="Data points"
            ),
            go.Scatter3d(
                x=frames[0][:, 0],
                y=frames[0][:, 1],
                z=frames[0][:, 2],
                mode="markers",
                marker=dict(
                    color=["steelblue", "coral", "mediumseagreen"],
                    size=12,
                    symbol="cross",
                    line=dict(width=3)
                ),
                name="Centroids"
            )
        ],
        frames=fig_frames
    )

    fig.update_layout(
        title="K-Means Clustering 3D — watch the centroids fly!",
        scene=dict(
            xaxis_title="Feature 1",
            yaxis_title="Feature 2",
            zaxis_title="Feature 3"
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[
                dict(label="Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 800}, "fromcurrent": True}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"mode": "immediate"}])
            ]
        )],
        sliders=[dict(
            steps=[
                dict(method="animate",
                     args=[[f"Iteration {i+1}"], {"mode": "immediate"}],
                     label=f"Step {i+1}")
                for i in range(10)
            ]
        )]
    )

    fig.show()

def show_decision_tree():

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.datasets import make_classification
    import plotly.graph_objects as go

    np.random.seed(42)

    X, y = make_classification(
        n_samples=200,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_clusters_per_class=1,
        random_state=42
    )

    feature_names = ["Cloud Cover", "Humidity"]
    class_names = ["No Rain", "Rain"]

    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)

    tree = clf.tree_

    # --- Build node positions ---
    node_x = {}
    node_y = {}
    node_labels = {}

    def get_label(node_id):
        if tree.children_left[node_id] == -1:
            # Leaf node
            class_idx = np.argmax(tree.value[node_id])
            return f"✅ {class_names[class_idx]}"
        else:
            feature = feature_names[tree.feature[node_id]]
            threshold = tree.threshold[node_id]
            return f"{feature}\n≤ {threshold:.2f}?"

    def assign_positions(node_id, depth, left, right):
        mid = (left + right) / 2
        node_x[node_id] = mid
        node_y[node_id] = -depth

        if tree.children_left[node_id] != -1:
            assign_positions(tree.children_left[node_id],  depth + 1, left, mid)
            assign_positions(tree.children_right[node_id], depth + 1, mid, right)

        node_labels[node_id] = get_label(node_id)

    assign_positions(0, 0, 0, 1)

    # --- Draw edges ---
    edge_x = []
    edge_y = []

    for node_id in range(tree.node_count):
        left  = tree.children_left[node_id]
        right = tree.children_right[node_id]

        if left != -1:
            edge_x += [node_x[node_id], node_x[left],  None]
            edge_y += [node_y[node_id], node_y[left],  None]
        if right != -1:
            edge_x += [node_x[node_id], node_x[right], None]
            edge_y += [node_y[node_id], node_y[right], None]

    # --- Node colors ---
    node_colors = []
    for node_id in range(tree.node_count):
        if tree.children_left[node_id] == -1:
            class_idx = np.argmax(tree.value[node_id])
            node_colors.append("lightblue" if class_idx == 0 else "lightsalmon")
        else:
            node_colors.append("lightyellow")

    fig = go.Figure()

    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="gray", width=1.5),
        hoverinfo="none",
        showlegend=False
    ))

    # Nodes
    fig.add_trace(go.Scatter(
        x=[node_x[i] for i in range(tree.node_count)],
        y=[node_y[i] for i in range(tree.node_count)],
        mode="markers+text",
        marker=dict(
            size=40,
            color=node_colors,
            line=dict(color="gray", width=1.5)
        ),
        text=[node_labels[i] for i in range(tree.node_count)],
        textposition="middle center",
        textfont=dict(size=9),
        hoverinfo="text",
        showlegend=False
    ))

    # Yes / No edge labels
    for node_id in range(tree.node_count):
        left  = tree.children_left[node_id]
        right = tree.children_right[node_id]

        if left != -1:
            mid_x = (node_x[node_id] + node_x[left])  / 2
            mid_y = (node_y[node_id] + node_y[left])   / 2
            fig.add_annotation(x=mid_x, y=mid_y, text="Yes",
                               showarrow=False, font=dict(color="green", size=11))

        if right != -1:
            mid_x = (node_x[node_id] + node_x[right]) / 2
            mid_y = (node_y[node_id] + node_y[right])  / 2
            fig.add_annotation(x=mid_x, y=mid_y, text="No",
                               showarrow=False, font=dict(color="red", size=11))

    fig.update_layout(
        title="Decision Tree — follow the questions to reach an answer",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white",
        height=600
    )

    fig.show()