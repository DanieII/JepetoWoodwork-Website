const slider = document.querySelector("#slider");
const minPriceInput = document.querySelector("#id_min_price");
const maxPriceInput = document.querySelector("#id_max_price");
const sliderValuesElement = document.querySelector("#slider-values");
sliderValuesElement.textContent = `${parseInt(
  minPriceInput.value,
)} лв. - ${parseInt(maxPriceInput.value)} лв.`;

noUiSlider.create(slider, {
  start: [0, 500],
  connect: true,
  step: 10,
  range: {
    min: 0,
    max: 500,
  },
});

slider.noUiSlider.on("update", function (values, handle) {
  const [minPrice, maxPrice] = values;
  minPriceInput.value = minPrice;
  maxPriceInput.value = maxPrice;
  sliderValuesElement.textContent = `${parseInt(minPrice)} лв. - ${parseInt(
    maxPrice,
  )} лв.`;
});
