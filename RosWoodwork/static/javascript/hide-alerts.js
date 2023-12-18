const alerts = document.querySelectorAll(".alert");

alerts.forEach((alert) => {
  const animationDuration = 500;
  const displayTime = 2500;
  setTimeout(function () {
    alert.classList.add("fade");
    setTimeout(function () {
      alert.remove();
    }, animationDuration);
  }, displayTime);
});
