// const deliverySelect = document.querySelector(".form select");
// const orderInformation = document.querySelector(".order-information");
// const totalPrice = document.querySelector(".total-price");
// const totalPriceNumber = parseFloat(totalPrice.textContent);
// const courierPrice = 7;

// function addDisabledToField() {
//   disabledOption = document.querySelector(".form select option:first-of-type");
//   disabledOption.disabled = true;
// }
// addDisabledToField();

// function setTotalPrice(newPrice) {
//   totalPrice.textContent = newPrice;
// }

// function addCourierPrice() {
//   const courierPriceElement = document.createElement("p");
//   courierPriceElement.classList.add("courier-price");
//   const boldText = document.createElement("b");
//   boldText.textContent = "7.00 лв.";

//   courierPriceElement.textContent = "Куриер - ";
//   courierPriceElement.appendChild(boldText);

//   orderInformation.insertBefore(
//     courierPriceElement,
//     totalPrice.parentElement.parentElement,
//   );
//   setTotalPrice(totalPriceNumber + courierPrice);
// }

// function removeCourierPrice() {
//   const courierPriceElement = document.querySelector(".courier-price");
//   if (courierPriceElement) {
//     courierPriceElement.remove();
//     setTotalPrice(totalPriceNumber);
//   }
// }

// function handleDeliveryType() {
//   const selectedValue = deliverySelect.value;

//   if (selectedValue === "courier") {
//     addCourierPrice();
//   } else {
//     removeCourierPrice();
//   }
// }

// document.addEventListener("DOMContentLoaded", handleDeliveryType);
// deliverySelect.addEventListener("change", handleDeliveryType);
