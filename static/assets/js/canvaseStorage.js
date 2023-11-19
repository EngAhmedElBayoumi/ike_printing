document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("tshirt-canvas-front");
  const ctx = canvas.getContext("2d");
  let isDrawing = false;
  let lastX = 0;
  let lastY = 0;

  // Retrieve stored actions from local storage (on page load)
  function loadCanvasActions() {
    const savedCanvasActions = localStorage.getItem("savedCanvasActions");
    if (savedCanvasActions) {
      const storedActions = JSON.parse(savedCanvasActions);
      storedActions.forEach(action => {
        if (action.type === "draw") {
          drawLine(action.startX, action.startY, action.endX, action.endY);
        }
        // Handle other types of actions if needed
      });
    }
  }

  // Function to save canvas actions in local storage
  function saveCanvasActions() {
    localStorage.setItem("savedCanvasActions", JSON.stringify(canvasActions));
  }

  // Function to draw a line on the canvas
  function drawLine(startX, startY, endX, endY) {
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.stroke();
  }

  // Function to record drawing actions
  function recordDrawingAction(startX, startY, endX, endY) {
    const canvasActions = JSON.parse(localStorage.getItem("savedCanvasActions")) || [];

    canvasActions.push({
      type: "draw",
      startX,
      startY,
      endX,
      endY
    });

    localStorage.setItem("savedCanvasActions", JSON.stringify(canvasActions));

    // Alert when an action is performed
    alert("Action performed!");
  }

  // Event listeners for mouse movement
  canvas.addEventListener("mousedown", e => {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
  });
  canvas.addEventListener("mousemove", e => {
    if (isDrawing) {
      const [currentX, currentY] = [e.offsetX, e.offsetY];
      drawLine(lastX, lastY, currentX, currentY);
      recordDrawingAction(lastX, lastY, currentX, currentY);
      [lastX, lastY] = [currentX, currentY];
    }
  });
  canvas.addEventListener("mouseup", () => {
    isDrawing = false;
  });

  // Load stored canvas actions on page load
  loadCanvasActions();
});
