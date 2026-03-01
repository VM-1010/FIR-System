(function () {
  "use strict";

  function animateIn(elements) {
    elements.forEach(function (el, index) {
      el.style.opacity = "0";
      el.style.transform = "translateY(8px)";
      el.style.transition = "opacity 220ms ease, transform 220ms ease";
      window.setTimeout(function () {
        el.style.opacity = "1";
        el.style.transform = "translateY(0)";
      }, index * 30);
    });
  }

  function addHoverLift(elements) {
    elements.forEach(function (el) {
      el.style.transition = "transform 160ms ease, box-shadow 160ms ease";
      el.addEventListener("mouseenter", function () {
        el.style.transform = "translateY(-2px)";
        el.style.boxShadow = "0 10px 18px rgba(0, 0, 0, 0.08)";
      });
      el.addEventListener("mouseleave", function () {
        el.style.transform = "translateY(0)";
        el.style.boxShadow = "";
      });
    });
  }

  function wireModalClose(modalId, closeIds) {
    var modal = document.getElementById(modalId);
    if (!modal) {
      return;
    }

    function closeModal() {
      modal.classList.add("hidden");
    }

    closeIds.forEach(function (id) {
      var btn = document.getElementById(id);
      if (btn) {
        btn.addEventListener("click", closeModal);
      }
    });

    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        closeModal();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !modal.classList.contains("hidden")) {
        closeModal();
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var cards = Array.prototype.slice.call(document.querySelectorAll(".stat-card, .panel-card, .card-lite"));
    var actions = Array.prototype.slice.call(document.querySelectorAll(".quick-action"));

    animateIn(cards.concat(actions));
    addHoverLift(actions);
    wireModalClose("confirmModal", ["cancelUpdateBtn", "confirmUpdateBtn"]);
  });
})();
