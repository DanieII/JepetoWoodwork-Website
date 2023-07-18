const stars = document.querySelectorAll(".star-rating i");
const ratingInput = document.querySelector("input[name='rating']");
let selectedRating = 0;

function handleStarHover(event) {
  const hoveredRating = event.target.getAttribute("rating-value");
  resetStars();
  fillStars(hoveredRating);
}

function resetStars() {
  stars.forEach((star, index) => {
    if (index >= 1) {
      if (index < selectedRating) {
        star.classList.add("fa-solid");
      } else {
        star.classList.remove("fa-solid");
      }
    }
  });
}

function fillStars(rating) {
  stars.forEach((star, index) => {
    if (index < rating) {
      star.classList.add("fa-solid");
    }
  });
}

stars.forEach((star) => {
  star.addEventListener("mouseenter", handleStarHover);
  star.addEventListener("click", () => {
    selectedRating = parseInt(star.getAttribute("rating-value"));
    ratingInput.value = selectedRating;
  });
});

document
  .querySelector(".star-rating")
  .addEventListener("mouseleave", resetStars);
