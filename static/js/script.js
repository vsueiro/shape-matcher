document.addEventListener("DOMContentLoaded", function () {
  let canvas = document.getElementById("drawingCanvas");
  let similarPlaces = document.getElementById("similarPlaces");
  let ctx = canvas.getContext("2d");

  // Fill the canvas with a white background
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  let drawing = false;

  function startPosition(e) {
    drawing = true;
    draw(e);
  }

  function endPosition() {
    drawing = false;
    ctx.beginPath();
  }

  function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = 10;
    ctx.lineCap = "round";
    ctx.strokeStyle = "black";

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  }

  canvas.addEventListener("mousedown", startPosition);
  canvas.addEventListener("mouseup", endPosition);
  canvas.addEventListener("mousemove", draw);

  document.getElementById("submitBtn").addEventListener("click", function () {
    const dataUrl = canvas.toDataURL("image/png");
    fetch("/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: dataUrl }),
    })
      .then((response) => response.json())
      .then((places) => {
        similarPlaces.replaceChildren();

        places.forEach((place, index) => {
          let markup = `
            <li>
              <figure>

                <img src="static/shapes/${place[0]}">
                <figcaption>
                  <h3>
                    ${index + 1}. ${place[0]}
                  </h3>
                  <p>
                    Similarity: ${Math.round(place[1] * 100)}%
                  </p>
                </figcaption>
              </figure>
            </li>
          `;
          similarPlaces.insertAdjacentHTML("beforeend", markup);
        });

        console.log("Response:", places);
      });
  });
});
