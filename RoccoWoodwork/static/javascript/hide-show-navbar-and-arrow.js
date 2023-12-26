const backToTopArrow = document.querySelector(".back-to-top");

backToTopArrow.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});
