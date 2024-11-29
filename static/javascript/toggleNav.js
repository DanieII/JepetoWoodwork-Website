const navBtn = document.querySelector(".nav-btn");
const navLinks = document.querySelector(".nav-links");
const nav = document.querySelector("nav");

navBtn.addEventListener("click", toggleNav);

function toggleNav() {
    navLinks.classList.toggle("active");
    navBtn.classList.toggle("active");
    nav.classList.toggle("active");
    nav.classList.remove("transparent");

    toggleOverlay();

    if (typeof changeNavColor !== "undefined") {
        changeNavColor();
    }
}

function createOverlay() {
    const overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.addEventListener("click", toggleNav);

    document.body.appendChild(overlay);
}

function toggleOverlay() {
    const overlay = document.querySelector(".overlay");

    if (overlay) {
        overlay.remove();
    } else {
        createOverlay();
    }
}
