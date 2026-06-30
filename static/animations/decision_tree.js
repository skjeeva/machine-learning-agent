function animateDecisionTree() {
  const plot = document.getElementById("plot");
  const plot2 = document.getElementById("plot2");

  // ===== PART 1: 2D tree diagram (same as before) =====

  const nodes = [
    { id: 0, x: 0.5, y: 0,    label: "Cloudy?",        type: "question" },
    { id: 1, x: 0.25, y: -1,  label: "Humidity high?", type: "question" },
    { id: 2, x: 0.75, y: -1,  label: "No Rain",        type: "leaf-no" },
    { id: 3, x: 0.1, y: -2,   label: "Rain",           type: "leaf-yes" },
    { id: 4, x: 0.4, y: -2,   label: "No Rain",        type: "leaf-no" }
  ];

  const edges = [
    { from: 0, to: 1, label: "Yes" },
    { from: 0, to: 2, label: "No" },
    { from: 1, to: 3, label: "Yes" },
    { from: 1, to: 4, label: "No" }
  ];

  const colorMap = {
    "question": "#fff3b0",
    "leaf-no": "#a8d0f0",
    "leaf-yes": "#f5b0a0"
  };

  const treeFrames = [];
  const revealOrder = [0, 1, 2, 3, 4];

  for (let step = 1; step <= revealOrder.length; step++) {
    const visibleIds = revealOrder.slice(0, step);
    const visibleNodes = nodes.filter(n => visibleIds.includes(n.id));

    const edgeX = [];
    const edgeY = [];
    const annotations = [];

    edges.forEach(e => {
      if (visibleIds.includes(e.from) && visibleIds.includes(e.to)) {
        const a = nodes[e.from];
        const b = nodes[e.to];
        edgeX.push(a.x, b.x, null);
        edgeY.push(a.y, b.y, null);
        annotations.push({
          x: (a.x + b.x) / 2,
          y: (a.y + b.y) / 2,
          text: e.label,
          showarrow: false,
          font: { color: e.label === "Yes" ? "green" : "red", size: 12 }
        });
      }
    });

    treeFrames.push({
      name: `step${step}`,
      data: [
        { x: edgeX, y: edgeY, mode: "lines", line: { color: "gray", width: 2 }, hoverinfo: "none" },
        {
          x: visibleNodes.map(n => n.x),
          y: visibleNodes.map(n => n.y),
          mode: "markers+text",
          marker: { size: 60, color: visibleNodes.map(n => colorMap[n.type]), line: { color: "gray", width: 1 } },
          text: visibleNodes.map(n => n.label),
          textposition: "middle center",
          textfont: { size: 11 }
        }
      ],
      layout: { annotations: annotations }
    });
  }

  const treeLayout = {
    title: "Decision Tree — built question by question",
    xaxis: { showgrid: false, zeroline: false, showticklabels: false, range: [-0.1, 1.1] },
    yaxis: { showgrid: false, zeroline: false, showticklabels: false, range: [-2.5, 0.5] },
    plot_bgcolor: "white",
    updatemenus: [{
      type: "buttons",
      buttons: [
        { label: "▶ Play", method: "animate", args: [null, { frame: { duration: 900 }, fromcurrent: true }] },
        { label: "⏸ Pause", method: "animate", args: [[null], { mode: "immediate" }] },
        { label: "↺ Restart", method: "animate", args: [["step1"], { mode: "immediate" }] }
      ]
    }],
    sliders: [{
      steps: treeFrames.map((f, i) => ({
        method: "animate",
        args: [[`step${i + 1}`], { mode: "immediate" }],
        label: `${i + 1}`
      })),
      currentvalue: { prefix: "Step: " }
    }]
  };

  Plotly.newPlot(plot, treeFrames[0].data, treeLayout).then(() => {
    Plotly.addFrames(plot, treeFrames);
  });

  // ===== PART 2: 3D decision boundary surface =====
  // Two features: cloud cover (x) and humidity (y) -> predicted class as height (z)

  function predict(cloud, humidity) {
    // Mirrors the tree above: cloudy? -> humidity high? -> rain
    if (cloud > 5) {
      return humidity > 5 ? 1 : 0; // 1 = Rain, 0 = No Rain
    }
    return 0;
  }

  const resolution = 40;
  const cloudVals = [];
  const humidityVals = [];
  for (let i = 0; i <= resolution; i++) {
    cloudVals.push((i / resolution) * 10);
    humidityVals.push((i / resolution) * 10);
  }

  const zBoundary = humidityVals.map(h =>
    cloudVals.map(c => predict(c, h))
  );

  const boundarySurface = {
    type: "surface",
    x: cloudVals,
    y: humidityVals,
    z: zBoundary,
    colorscale: [[0, "lightblue"], [1, "lightsalmon"]],
    showscale: false,
    opacity: 0.85,
    name: "Predicted class"
  };

  const boundaryLayout = {
    title: "Decision Boundary in 3D — where the tree predicts Rain vs No Rain",
    scene: {
      xaxis: { title: "Cloud Cover" },
      yaxis: { title: "Humidity" },
      zaxis: { title: "Prediction (0 = No Rain, 1 = Rain)", range: [0, 1] }
    }
  };

  Plotly.newPlot(plot2, [boundarySurface], boundaryLayout);
}