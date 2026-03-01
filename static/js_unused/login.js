(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var card = document.querySelector(".auth-card");
    var inputs = Array.prototype.slice.call(document.querySelectorAll("#loginForm input"));
    var button = document.querySelector("#loginForm button[type='submit']");

    if (card) {
      card.style.opacity = "0";
      card.style.transform = "translateY(10px)";
      card.style.transition = "opacity 240ms ease, transform 240ms ease";
      window.setTimeout(function () {
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }, 40);
    }

    inputs.forEach(function (input) {
      input.style.transition = "box-shadow 160ms ease, border-color 160ms ease";
      input.addEventListener("focus", function () {
        input.style.boxShadow = "0 0 0 3px rgba(30, 100, 180, 0.15)";
      });
      input.addEventListener("blur", function () {
        input.style.boxShadow = "";
      });
    });

    if (button) {
      button.style.transition = "transform 140ms ease, box-shadow 140ms ease";
      button.addEventListener("mouseenter", function () {
        button.style.transform = "translateY(-1px)";
        button.style.boxShadow = "0 8px 16px rgba(0, 0, 0, 0.12)";
      });
      button.addEventListener("mouseleave", function () {
        button.style.transform = "translateY(0)";
        button.style.boxShadow = "";
      });
      button.addEventListener("mousedown", function () {
        button.style.transform = "translateY(0) scale(0.99)";
      });
      button.addEventListener("mouseup", function () {
        button.style.transform = "translateY(-1px)";
      });
    }
  });
})();
