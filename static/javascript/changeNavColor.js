const homeNavBar = document.querySelector("nav");
const navBarHeight = homeNavBar.clientHeight;
const homeProductsToggle = document.querySelector(".products-toggle");

homeNavBar.classList.add("transparent");

document.addEventListener("scroll", changeNavColor);

function changeNavColor() {
    if (
        homeNavBar.classList.contains("active") ||
        homeProductsToggle.classList.contains("active")
    ) {
        return;
    }

    const yPosition = window.scrollY;

    if (yPosition > navBarHeight) {
        homeNavBar.classList.remove("transparent");
    } else {
        homeNavBar.classList.add("transparent");
    }
}
