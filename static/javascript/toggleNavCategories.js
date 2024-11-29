const navBar = document.querySelector("nav");
const productsToggle = document.querySelector(".products-toggle");

productsToggle.addEventListener("click", () => {
    productsToggle.classList.toggle("active");

    if (navBar.classList.contains("transparent")) {
        navBar.classList.remove("transparent");
    } else {
        if (typeof changeNavColor !== "undefined") {
            changeNavColor();
        }
    }
});
