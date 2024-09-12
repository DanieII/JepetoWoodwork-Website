const imageElements = document.querySelectorAll(".image-container img");

for (const imageElement of imageElements) {
  imageElement.addEventListener("click", handleImageElementClick);
}

function handleImageElementClick(e) {
  const overlay = document.createElement("div");
  const imageElementCopy = e.target.cloneNode();

  overlay.className = "overlay";
  overlay.addEventListener("click", (e) => e.currentTarget.remove());

  overlay.appendChild(imageElementCopy);
  document.body.appendChild(overlay);
}
