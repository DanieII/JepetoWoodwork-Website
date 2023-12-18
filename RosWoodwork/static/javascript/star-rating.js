const stars = document.querySelectorAll(".star-rating i");
const ratingInput = document.querySelector("input[name='rating']");
const formStarInput = document.querySelector(".stars-field");
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

function setPreviousStars() {
  previousValue = formStarInput.value;
  ratingInput.value = previousValue;
  selectedRating = previousValue;
  fillStars(previousValue);
}

stars.forEach((star) => {
  star.addEventListener("mouseenter", handleStarHover);
  star.addEventListener("click", () => {
    selectedRating = parseInt(star.getAttribute("rating-value"));
    ratingInput.value = selectedRating;
    formStarInput.value = selectedRating;
    resetStars();
  });
});

document
  .querySelector(".star-rating")
  .addEventListener("mouseleave", resetStars);

document.addEventListener("DOMContentLoaded", setPreviousStars());
