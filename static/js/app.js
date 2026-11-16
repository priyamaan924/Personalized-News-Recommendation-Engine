document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert").forEach((alert) => {
    setTimeout(() => { alert.style.opacity = "0"; alert.style.transition = "opacity .5s"; }, 4500);
  });
});
