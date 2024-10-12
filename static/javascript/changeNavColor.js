const navBar = document.querySelector("nav");
const navBarHeight = navBar.clientHeight;

navBar.classList.add("transparent");

document.addEventListener("scroll", changeNavColor);

function changeNavColor() {
  if (navBar.classList.contains("active")) {
    return;
  }

  const yPosition = window.scrollY;

  if (yPosition > navBarHeight) {
    navBar.classList.remove("transparent");
  } else {
    navBar.classList.add("transparent");
  }
}
