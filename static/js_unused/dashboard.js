(function () {
  const role = localStorage.getItem("role");
  const container = document.getElementById("routeContainer");
  const message = document.getElementById("dashboardMsg");

  if (!container) return;

  function renderButton(label, target) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn btn-primary";
    button.textContent = label;
    button.addEventListener("click", function () {
      window.location.href = target;
    });
    container.innerHTML = "";
    container.appendChild(button);
  }

  if (role === "officer") {
    renderButton("Go to Officer Panel", "officer.html");
    return;
  }

  if (role === "admin") {
    renderButton("Go to Admin Panel", "admin.html");
    return;
  }

  message.textContent = "No role found. Please login first.";
  const loginLink = document.createElement("a");
  loginLink.href = "login.html";
  loginLink.className = "link";
  loginLink.textContent = "Back to Login";
  container.innerHTML = "";
  container.appendChild(loginLink);
})();
