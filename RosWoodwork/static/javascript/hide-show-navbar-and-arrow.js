let prevScrollPos = window.pageYOffset;
const nav = document.querySelector("nav");
const navHeight = nav.offsetHeight;
const navbar = document.querySelector(".nav-wrapper");
const navMenu = document.querySelector(".navigation-menu");
const backToTopArrow = document.querySelector(".back-to-top");

backToTopArrow.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

window.onscroll = function () {
  let currentScrollPos = window.scrollY;

  if (currentScrollPos <= navHeight) {
    navbar.classList.remove("hidden");
    backToTopArrow.classList.remove("active");
  } else {
    if (prevScrollPos > currentScrollPos) {
      navbar.classList.remove("hidden");
    } else {
      navbar.classList.add("hidden");
      if (navMenu.classList.contains("active")) {
        navMenu.classList.remove("active");
        hamburger.classList.remove("active");
      }
      backToTopArrow.classList.add("active");
    }
  }

  prevScrollPos = currentScrollPos;
};
