let prevScrollPos = window.pageYOffset;
const navbar = document.querySelector(".nav-wrapper");
const navMenu = document.querySelector(".navigation-menu");
const navbarHeight = 100;

window.onscroll = function () {
  let currentScrollPos = window.pageYOffset;
  console.log(currentScrollPos);

  if (currentScrollPos <= navbarHeight) {
    navbar.classList.remove("hidden");
  } else {
    if (prevScrollPos > currentScrollPos) {
      navbar.classList.remove("hidden");
    } else {
      navbar.classList.add("hidden");
      if (navMenu.classList.contains("active")) {
        navMenu.classList.remove("active");
        hamburger.classList.remove("active");
      }
    }
  }

  prevScrollPos = currentScrollPos;
};
