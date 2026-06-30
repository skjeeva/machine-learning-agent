function animateLinearRegression() {
  const plot = document.getElementById("plot");

  // --- Generate data: price depends on size AND rooms ---
  const n = 60;
  const x1 = []; // house size
  const x2 = []; // rooms
  const yTrue = []; // price

  for (let i = 0; i < n; i++) {
    const size = Math.random() * 10;
    const rooms = Math.random() * 5;
    x1.push(size);
    x2.push(rooms);
    yTrue.push(2 * size + 3 * rooms + 1 + (Math.random() - 0.5) * 4);
  }

  // --- Compute the real best-fit plane using least squares ---
  // Solve for [m1, m2, b] in y = m1*x1 + m2*x2 + b
  function fitPlane(x1, x2, y) {
    const n = x1.length;
    let sx1 = 0, sx2 = 0, sy = 0, sx1x1 = 0, sx2x2 = 0, sx1x2 = 0, sx1y = 0, sx2y = 0;

    for (let i = 0; i < n; i++) {
      sx1 += x1[i]; sx2 += x2[i]; sy += y[i];
      sx1x1 += x1[i] * x1[i];
      sx2x2 += x2[i] * x2[i];
      sx1x2 += x1[i] * x2[i];
      sx1y += x1[i] * y[i];
      sx2y += x2[i] * y[i];
    }

    // Normal equations (3x3 system) solved via Cramer's rule
    const A = [
      [sx1x1, sx1x2, sx1],
      [sx1x2, sx2x2, sx2],
      [sx1, sx2, n]
    ];
    const B = [sx1y, sx2y, sy];

    function det3(m) {
      return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
        m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
        m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
      );
    }

    function replaceCol(m, col, vec) {
      return m.map((row, i) => row.map((val, j) => (j === col ? vec[i] : val)));
    }

    const d = det3(A);
    const m1 = det3(replaceCol(A, 0, B)) / d;
    const m2 = det3(replaceCol(A, 1, B)) / d;
    const b = det3(replaceCol(A, 2, B)) / d;

    return { m1, m2, b };
  }

  const { m1: m1Final, m2: m2Final, b: bFinal } = fitPlane(x1, x2, yTrue);

  // Start from a deliberately wrong plane
  const m1Start = -2, m2Start = -2, bStart = 30;

  const steps = 20;
  const frames = [];

  // Grid for the plane surface
  const gridX1 = [];
  const gridX2 = [];
  for (let i = 0; i <= 15; i++) {
    gridX1.push((i / 15) * 10);
    gridX2.push((i / 15) * 5);
  }

  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const m1 = m1Start + (m1Final - m1Start) * t;
    const m2 = m2Start + (m2Final - m2Start) * t;
    const b = bStart + (bFinal - bStart) * t;

    const zSurface = gridX2.map(g2 =>
      gridX1.map(g1 => m1 * g1 + m2 * g2 + b)
    );

    frames.push({
      name: `step${i}`,
      data: [
        {
          type: "scatter3d",
          x: x1, y: x2, z: yTrue,
          mode: "markers",
          marker: { color: "steelblue", size: 4 },
          name: "Data points"
        },
        {
          type: "surface",
          x: gridX1, y: gridX2, z: zSurface,
          opacity: 0.6,
          colorscale: "Reds",
          showscale: false,
          name: "Fitted plane"
        }
      ]
    });
  }

  const layout = {
    title: "Linear Regression in 3D — plane fitting two features",
    scene: {
      xaxis: { title: "House size" },
      yaxis: { title: "Rooms" },
      zaxis: { title: "Price" }
    },
    updatemenus: [{
      type: "buttons",
      buttons: [
        { label: "▶ Play", method: "animate", args: [null, { frame: { duration: 300 }, fromcurrent: true }] },
        { label: "⏸ Pause", method: "animate", args: [[null], { mode: "immediate" }] },
        { label: "↺ Restart", method: "animate", args: [["step0"], { mode: "immediate" }] }
      ]
    }],
    sliders: [{
      steps: frames.map((f, i) => ({
        method: "animate",
        args: [[`step${i}`], { mode: "immediate" }],
        label: `${i}`
      })),
      currentvalue: { prefix: "Step: " }
    }]
  };

  Plotly.newPlot(plot, frames[0].data, layout).then(() => {
    Plotly.addFrames(plot, frames);
  });
}