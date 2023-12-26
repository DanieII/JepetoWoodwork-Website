const navBar = document.querySelector(".main-nav");
const navBarHeight = navBar.clientHeight;
const [whiteLogo, darkLogo] = document.querySelectorAll(".logo-container img");

navBar.classList.add("transparent");

document.addEventListener("scroll", handleScroll);

function handleScroll() {
  const yPosition = window.scrollY;

  if (navBar.classList.contains("active")) {
    return;
  }

  if (yPosition > navBarHeight) {
    navBar.classList.remove("transparent");
    whiteLogo.style.display = "block";
    darkLogo.style.display = "none";
  } else {
    navBar.classList.add("transparent");
    whiteLogo.style.display = "none";
    darkLogo.style.display = "block";
  }
}
