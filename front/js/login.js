(function () {
  const form = document.getElementById("loginForm");
  const message = document.getElementById("loginMsg");

  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const officerId = document.getElementById("officerId")?.value.trim() || "";
    const stationId = document.getElementById("stationId")?.value.trim() || "";
    const password = document.getElementById("password")?.value || "";

    if (!officerId || !stationId || !password) {
      message.textContent = "Please fill all fields.";
      return;
    }

    if (officerId.toLowerCase() === "admin@test.com") {
      localStorage.setItem("role", "admin");
    } else {
      localStorage.setItem("role", "officer");
    }

    window.location.href = "dashboard.html";
  });
})();
