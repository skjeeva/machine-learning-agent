from tools.visualizer import show_kmeans, show_kmeans_3d

def teach():

    print("\n===== K-MEANS CLUSTERING =====\n")

    print("""
Imagine you walk into a room full of people and you have to group them
into 3 groups — but you don't know anything about them yet.

So you randomly pick 3 people as "group leaders" (centroids).

Then everyone moves to the closest leader.

Then each leader moves to the center of their group.

Repeat until nobody moves anymore.

That's exactly how K-Means works.
""")

    show_kmeans()
    show_kmeans_3d()

    print("\nQuiz:")
    print("What does K represent in K-Means?")