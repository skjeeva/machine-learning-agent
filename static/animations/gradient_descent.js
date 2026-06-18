function animateGradientDescent() {
  const plot = document.getElementById("plot");

  // --- Data ---
  const x = [];
  const y = [];
  for (let i = -3; i <= 3; i += 0.05) {
    x.push(i);
    y.push(i * i); // simple parabola y = x²
  }

  // Gradient descent steps
  let pos = 2.8;
  const lr = 0.2;
  const steps = [];

  for (let i = 0; i < 20; i++) {
    steps.push({ x: pos, y: pos * pos });
    const grad = 2 * pos; // derivative of x²
    pos = pos - lr * grad;
  }

  // --- Base curve ---
  const curve = {
    x: x,
    y: y,
    mode: "lines",
    line: { color: "steelblue", width: 3 },
    name: "Loss curve"
  };

  // --- Frames ---
  const frames = steps.map((step, i) => ({
    name: `step${i}`,
    data: [
      curve,
      {
        x: steps.slice(0, i + 1).map(s => s.x),
        y: steps.slice(0, i + 1).map(s => s.y),
        mode: "lines+markers",
        line: { color: "coral", width: 2, dash: "dot" },
        marker: { color: "coral", size: 8 },
        name: "Path"
      },
      {
        x: [step.x],
        y: [step.y],
        mode: "markers+text",
        marker: { color: "red", size: 16 },
        text: [`Step ${i + 1}\nLoss: ${step.y.toFixed(3)}`],
        textposition: "top right",
        textfont: { size: 13, color: "red" },
        name: "Current position"
      }
    ]
  }));

  // --- Layout ---
  const layout = {
    title: "Gradient Descent — ball rolling down the loss curve",
    xaxis: { title: "Parameter value", range: [-3.5, 3.5] },
    yaxis: { title: "Loss", range: [-0.5, 9] },
    plot_bgcolor: "white",
    updatemenus: [{
      type: "buttons",
      buttons: [
        {
          label: "▶ Play",
          method: "animate",
          args: [null, { frame: { duration: 500 }, fromcurrent: true }]
        },
        {
          label: "⏸ Pause",
          method: "animate",
          args: [[null], { mode: "immediate" }]
        },
        {
          label: "↺ Restart",
          method: "animate",
          args: [["step0"], { mode: "immediate" }]
        }
      ]
    }],
    sliders: [{
      steps: steps.map((_, i) => ({
        method: "animate",
        args: [[`step${i}`], { mode: "immediate" }],
        label: `Step ${i + 1}`
      })),
      currentvalue: {
        prefix: "Step: ",
        font: { size: 14 }
      }
    }]
  };

  Plotly.newPlot(plot, [curve], layout).then(() => {
    Plotly.addFrames(plot, frames);
  });
}