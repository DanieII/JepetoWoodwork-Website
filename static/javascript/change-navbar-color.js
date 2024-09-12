const navBar = document.querySelector("nav");
const navBarHeight = navBar.clientHeight;

navBar.classList.add("transparent");

document.addEventListener("scroll", handleScroll);

function handleScroll() {
  const yPosition = window.scrollY;

  if (navBar.classList.contains("active")) {
    return;
  }

  if (yPosition > navBarHeight) {
    navBar.classList.remove("transparent");
  } else {
    navBar.classList.add("transparent");
  }
}
