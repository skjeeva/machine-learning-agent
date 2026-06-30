function animateKmeans() {
  const plot = document.getElementById("plot");

  function randNormal() {
    let u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  const data = [];
  const centers = [[2, 2, 2], [8, 8, 8], [2, 8, 5]];

  centers.forEach(c => {
    for (let i = 0; i < 40; i++) {
      data.push([
        c[0] + randNormal(),
        c[1] + randNormal(),
        c[2] + randNormal()
      ]);
    }
  });
  
  function distance(a, b) {
    return Math.sqrt(
      (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
    );
  }

  const shuffled = [...data].sort(() => Math.random() - 0.5);
  let centroids = [shuffled[0], shuffled[1], shuffled[2]];

  const colorMap = ["steelblue", "coral", "mediumseagreen"];
  const frames = [];
  const totalIterations = 10;

  for (let iter = 0; iter < totalIterations; iter++) {
    // Assign each point to nearest centroid
    const labels = data.map(point => {
      let best = 0, bestDist = Infinity;
      centroids.forEach((c, idx) => {
        const d = distance(point, c);
        if (d < bestDist) { bestDist = d; best = idx; }
      });
      return best;
    });

    const pointColors = labels.map(l => colorMap[l]);

    frames.push({
      name: `step${iter}`,
      data: [
        {
          type: "scatter3d",
          x: data.map(p => p[0]),
          y: data.map(p => p[1]),
          z: data.map(p => p[2]),
          mode: "markers",
          marker: { size: 4, color: pointColors },
          name: "Data points"
        },
        {
          type: "scatter3d",
          x: centroids.map(c => c[0]),
          y: centroids.map(c => c[1]),
          z: centroids.map(c => c[2]),
          mode: "markers",
          marker: { size: 10, color: colorMap, symbol: "diamond", line: { width: 2, color: "black" } },
          name: "Centroids"
        }
      ]
    });

    // Move centroids to mean of their assigned points
    centroids = centroids.map((c, idx) => {
      const assigned = data.filter((_, i) => labels[i] === idx);
      if (assigned.length === 0) return c;
      const meanX = assigned.reduce((s, p) => s + p[0], 0) / assigned.length;
      const meanY = assigned.reduce((s, p) => s + p[1], 0) / assigned.length;
      const meanZ = assigned.reduce((s, p) => s + p[2], 0) / assigned.length;
      return [meanX, meanY, meanZ];
    });
  }

  const layout = {
    title: "K-Means in 3D — watch centroids find the clusters",
    scene: {
      xaxis: { title: "Feature 1" },
      yaxis: { title: "Feature 2" },
      zaxis: { title: "Feature 3" }
    },
    updatemenus: [{
      type: "buttons",
      buttons: [
        { label: "▶ Play", method: "animate", args: [null, { frame: { duration: 700 }, fromcurrent: true }] },
        { label: "⏸ Pause", method: "animate", args: [[null], { mode: "immediate" }] },
        { label: "↺ Restart", method: "animate", args: [["step0"], { mode: "immediate" }] }
      ]
    }],
    sliders: [{
      steps: frames.map((f, i) => ({
        method: "animate",
        args: [[`step${i}`], { mode: "immediate" }],
        label: `${i + 1}`
      })),
      currentvalue: { prefix: "Iteration: " }
    }]
  };

  Plotly.newPlot(plot, frames[0].data, layout).then(() => {
    Plotly.addFrames(plot, frames);
  });
}