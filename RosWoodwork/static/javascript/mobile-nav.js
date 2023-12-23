const navBtn = document.querySelector(".nav-btn");
const navLinks = document.querySelector(".nav-links");
const nav = document.querySelector(".main-nav");

navBtn.addEventListener("click", toggleNav);
navBtn.addEventListener("touchstart", toggleNav);
const isHomePage = document.querySelector(".banner");

function toggleNav() {
  navLinks.classList.toggle("active");
  navBtn.classList.toggle("active");
  nav.classList.toggle("active");
  nav.classList.remove("transparent");

  toggleOverlay();

  if (isHomePage) {
    handleScroll();
  }
}

function toggleOverlay() {
  let overlay = document.querySelector(".overlay");

  if (overlay) {
    overlay.remove();
  } else {
    overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.addEventListener("click", toggleNav);
    overlay.addEventListener("touchstart", toggleNav);

    document.body.appendChild(overlay);
  }
}
