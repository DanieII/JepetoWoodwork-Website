const searchToggles = document.querySelectorAll(".search-toggle");
const search = document.querySelector(".search");

for (const toggle of searchToggles) {
	toggle.addEventListener("click", () => {
		search.classList.toggle("visible");
	});
}
