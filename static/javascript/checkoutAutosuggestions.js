const endpoints = {
  city: "http://demo.econt.com/ee/services/Nomenclatures/NomenclaturesService.getCities.json",
  address:
    "http://demo.econt.com/ee/services/Nomenclatures/NomenclaturesService.getOffices.json",
};

const demoUsername = "iasp-dev";
const demoPassword = "1Asp-dev";
const auth = btoa(`${demoUsername}:${demoPassword}`);

const autocompleteFields = document.querySelectorAll(".autocomplete");
const deliveryTypeField = document.querySelector('[name="delivery_type"]');

autocompleteFields.forEach((field) => {
  const fieldName = field.name;
  const url = endpoints[fieldName];
  let suggestions = [];

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${auth}`,
    },
    body: JSON.stringify({ countryCode: "BGR" }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (fieldName === "city") {
        suggestions = data.cities.map((city) => city.name);
      } else if (fieldName === "address") {
        suggestions = data.offices.map((office) => office.address.fullAddress);
      }

      setupAutocomplete(field, suggestions);
    })
    .catch((error) => {
      console.error(`Error fetching suggestions for ${fieldName}`, error);
    });
});

function setupAutocomplete(field, suggestions) {
  const autocompleteList = document.createElement("ul");
  autocompleteList.classList.add("autocomplete-suggestions");
  field.parentNode.appendChild(autocompleteList);

  field.addEventListener("input", () => {
    const query = field.value.toLowerCase();
    autocompleteList.innerHTML = "";

    if (query.length > 1) {
      // No suggestions for address if delivery type is not for office
      if (
        field.name === "address" &&
        deliveryTypeField.value === "Адрес на получател"
      ) {
        autocompleteList.innerHTML = "";
        return;
      }

      const filteredSuggestions = suggestions
        .filter((item) => item?.toLowerCase().includes(query))
        .slice(0, 10);

      filteredSuggestions.forEach((suggestion) => {
        const suggestionItem = document.createElement("li");
        suggestionItem.textContent = suggestion;
        suggestionItem.addEventListener("click", () => {
          field.value = suggestion;
          autocompleteList.innerHTML = "";
        });

        autocompleteList.appendChild(suggestionItem);
      });
    }
  });

  document.addEventListener("click", (e) => {
    if (!field.contains(e.target) && !autocompleteList.contains(e.target)) {
      autocompleteList.innerHTML = "";
    }
  });
}
