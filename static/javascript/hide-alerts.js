const alerts = document.querySelectorAll(".alert");
const displayTime = 2000;

alerts.forEach((alert) => {
  setTimeout(() => {
    alert.remove();
  }, displayTime);
});
