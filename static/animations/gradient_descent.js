function animateGradientDescent() {
  const plot = document.getElementById("plot");

  // --- Build the bowl surface: z = x² + y² ---
  const range = 3;
  const resolution = 40;
  const xs = [];
  const ys = [];
  for (let i = 0; i <= resolution; i++) {
    xs.push(-range + (2 * range * i) / resolution);
    ys.push(-range + (2 * range * i) / resolution);
  }

  const zSurface = ys.map(yVal =>
    xs.map(xVal => xVal * xVal + yVal * yVal)
  );

  const surface = {
    type: "surface",
    x: xs,
    y: ys,
    z: zSurface,
    colorscale: "Blues",
    opacity: 0.75,
    showscale: false,
    name: "Loss surface"
  };

  // --- Gradient descent path on the bowl ---
  let px = 2.6;
  let py = 2.2;
  const lr = 0.15;
  const steps = [];

  for (let i = 0; i < 18; i++) {
    const pz = px * px + py * py;
    steps.push({ x: px, y: py, z: pz });
    const gradX = 2 * px;
    const gradY = 2 * py;
    px = px - lr * gradX;
    py = py - lr * gradY;
  }

  // --- Frames ---
  const frames = steps.map((step, i) => ({
    name: `step${i}`,
    data: [
      surface,
      {
        type: "scatter3d",
        x: steps.slice(0, i + 1).map(s => s.x),
        y: steps.slice(0, i + 1).map(s => s.y),
        z: steps.slice(0, i + 1).map(s => s.z),
        mode: "lines+markers",
        line: { color: "orange", width: 4 },
        marker: { size: 3, color: "orange" },
        name: "Path"
      },
      {
        type: "scatter3d",
        x: [step.x],
        y: [step.y],
        z: [step.z],
        mode: "markers+text",
        marker: { size: 8, color: "red" },
        text: [`Step ${i + 1}<br>Loss: ${step.z.toFixed(2)}`],
        textposition: "top center",
        name: "Current"
      }
    ]
  }));

  const layout = {
    title: "Gradient Descent in 3D — ball rolling into the valley",
    scene: {
      xaxis: { title: "Parameter 1" },
      yaxis: { title: "Parameter 2" },
      zaxis: { title: "Loss" }
    },
    updatemenus: [{
      type: "buttons",
      buttons: [
        { label: "▶ Play", method: "animate", args: [null, { frame: { duration: 500 }, fromcurrent: true }] },
        { label: "⏸ Pause", method: "animate", args: [[null], { mode: "immediate" }] },
        { label: "↺ Restart", method: "animate", args: [["step0"], { mode: "immediate" }] }
      ]
    }],
    sliders: [{
      steps: steps.map((_, i) => ({
        method: "animate",
        args: [[`step${i}`], { mode: "immediate" }],
        label: `${i + 1}`
      })),
      currentvalue: { prefix: "Step: " }
    }]
  };

  Plotly.newPlot(plot, [surface], layout).then(() => {
    Plotly.addFrames(plot, frames);
  });
}