const alerts = document.querySelectorAll(".messages li");
const displayTime = 2000;

alerts.forEach((alert) => {
	setTimeout(() => {
		alert.remove();
	}, displayTime);
});
