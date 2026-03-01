(function () {
  "use strict";

  const state = {
    stationId: "S01",
    stationName: "Central Police Station",
    adminName: "Admin User",
    officers: [
      {
        officerId: "O01",
        name: "Rahul Sharma",
        rank: "Inspector",
        badgeNumber: "INSP1001",
        contactNumber: "9876543210",
        stationId: "S01"
      },
      {
        officerId: "O02",
        name: "Anita Singh",
        rank: "Sub Inspector",
        badgeNumber: "SI2002",
        contactNumber: "9988776655",
        stationId: "S01"
      },
      {
        officerId: "O03",
        name: "Vikram Das",
        rank: "Head Constable",
        badgeNumber: "HC3003",
        contactNumber: "9090909090",
        stationId: "S01"
      }
    ],
    firs: [
      {
        firId: "F01",
        firNumber: "2026-001",
        dateFiled: "2026-02-12",
        timeFiled: "09:45",
        place: "MG Road",
        description: "Theft reported near market area during evening hours.",
        status: "Under Investigation",
        complainant: {
          name: "Arjun Mehta",
          age: "34",
          gender: "Male",
          address: "14 Lake Street, City",
          contact: "9123456780",
          idProof: "Aadhaar"
        },
        officer: {
          name: "Rahul Sharma",
          rank: "Inspector",
          badgeNumber: "INSP1001",
          contactNumber: "9876543210",
          stationId: "S01"
        }
      },
      {
        firId: "F02",
        firNumber: "2026-002",
        dateFiled: "2026-02-15",
        timeFiled: "12:15",
        place: "Station Circle",
        description: "Vehicle damage complaint registered by complainant.",
        status: "Pending Review",
        complainant: {
          name: "Neha Patel",
          age: "29",
          gender: "Female",
          address: "22 Sunrise Colony, City",
          contact: "9012345678",
          idProof: "PAN Card"
        },
        officer: {
          name: "Anita Singh",
          rank: "Sub Inspector",
          badgeNumber: "SI2002",
          contactNumber: "9988776655",
          stationId: "S01"
        }
      },
      {
        firId: "F03",
        firNumber: "2026-003",
        dateFiled: "2026-02-18",
        timeFiled: "18:30",
        place: "River Bank",
        description: "Assault complaint with eyewitness statements recorded.",
        status: "Closed",
        complainant: {
          name: "Karan Verma",
          age: "42",
          gender: "Male",
          address: "8 Park Lane, City",
          contact: "9234567810",
          idProof: "Voter ID"
        },
        officer: {
          name: "Vikram Das",
          rank: "Head Constable",
          badgeNumber: "HC3003",
          contactNumber: "9090909090",
          stationId: "S01"
        }
      }
    ],
    pendingConfirmAction: null
  };

  const sections = {
    home: document.getElementById("adminHomeSection"),
    addOfficer: document.getElementById("addOfficerSection"),
    removeOfficer: document.getElementById("removeOfficerSection"),
    viewFir: document.getElementById("viewFirSection"),
    closeFir: document.getElementById("closeFirSection")
  };

  const confirmModal = document.getElementById("adminConfirmModal");
  const confirmMessage = document.getElementById("adminConfirmMessage");
  const confirmYesBtn = document.getElementById("adminConfirmYesBtn");
  const confirmNoBtn = document.getElementById("adminConfirmNoBtn");

  function setText(id, value) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = value;
    }
  }

  function showSection(sectionKey) {
    Object.keys(sections).forEach((key) => {
      if (sections[key]) {
        sections[key].classList.toggle("hidden", key !== sectionKey);
      }
    });
  }

  function clearFieldErrors(formId) {
    const form = document.getElementById(formId);
    if (!form) {
      return;
    }
    form.querySelectorAll(".field-error").forEach((err) => {
      err.textContent = "";
    });
  }

  function showConfirm(message, onConfirm) {
    state.pendingConfirmAction = onConfirm;
    confirmMessage.textContent = message;
    confirmModal.classList.remove("hidden");
  }

  function closeConfirm() {
    confirmModal.classList.add("hidden");
    state.pendingConfirmAction = null;
  }

  function getNextOfficerId() {
    const max = state.officers.reduce((acc, officer) => {
      const num = parseInt(officer.officerId.replace(/\D/g, ""), 10);
      return Number.isNaN(num) ? acc : Math.max(acc, num);
    }, 0);
    return `O${String(max + 1).padStart(2, "0")}`;
  }

  function populateHeaderContext() {
    setText("addOfficerStationName", state.stationName);
    setText("addOfficerAdminName", state.adminName);
    setText("removeOfficerStationName", state.stationName);
    setText("removeOfficerAdminName", state.adminName);
    setText("closeFirStationName", state.stationName);
    setText("closeFirAdminName", state.adminName);
    setText("mappingStationId", state.stationId);
    setText("mappingStationName", state.stationName);
    document.getElementById("addOfficerStationId").value = state.stationId;
  }

  function refreshStats() {
    const total = state.firs.length;
    const closed = state.firs.filter((fir) => fir.status === "Closed").length;
    const pending = state.firs.filter((fir) => fir.status === "Pending Review").length;
    const active = total - closed - pending;

    setText("adminStatTotal", String(total));
    setText("adminStatActive", String(active));
    setText("adminStatClosed", String(closed));
    setText("adminStatPending", String(pending));
  }

  function resetAddOfficerForm() {
    document.getElementById("addOfficerForm").reset();
    document.getElementById("addOfficerId").value = getNextOfficerId();
    document.getElementById("addOfficerStationId").value = state.stationId;
    document.getElementById("addOfficerSuccess").textContent = "";
    clearFieldErrors("addOfficerForm");
  }

  function refreshRemoveOfficerDropdown() {
    const select = document.getElementById("removeOfficerId");
    select.innerHTML = '<option value="">Select Officer ID</option>';
    state.officers.forEach((officer) => {
      const option = document.createElement("option");
      option.value = officer.officerId;
      option.textContent = officer.officerId;
      select.appendChild(option);
    });
  }

  function refreshCloseFirDropdown() {
    const select = document.getElementById("closeFirId");
    select.innerHTML = '<option value="">Select FIR ID</option>';
    state.firs.forEach((fir) => {
      const option = document.createElement("option");
      option.value = fir.firId;
      option.textContent = fir.firId;
      select.appendChild(option);
    });
  }

  function resetRemoveOfficerSection() {
    document.getElementById("removeOfficerId").value = "";
    document.getElementById("removeOfficerIdError").textContent = "";
    document.getElementById("removeOfficerSuccess").textContent = "";
    document.getElementById("removeOfficerDetailsBlock").classList.add("hidden");
    document.getElementById("deleteOfficerBtn").disabled = true;
    document.getElementById("removeOfficerHomeBtn").classList.add("hidden");
    [
      "removeOfficerName",
      "removeOfficerRank",
      "removeOfficerBadge",
      "removeOfficerContact",
      "removeOfficerStationId"
    ].forEach((id) => {
      document.getElementById(id).value = "";
    });
  }

  function resetViewFirSection() {
    document.getElementById("viewFirSearchInput").value = "";
    document.getElementById("viewFirError").textContent = "";
    document.getElementById("viewFirResultBlock").classList.add("hidden");
    [
      "viewFirNumber",
      "viewDateFiled",
      "viewTimeFiled",
      "viewPlace",
      "viewStatus",
      "viewDescription",
      "viewCompName",
      "viewCompAge",
      "viewCompGender",
      "viewCompAddress",
      "viewCompContact",
      "viewCompIdProof",
      "viewOfficerName",
      "viewOfficerRank",
      "viewOfficerBadge",
      "viewOfficerContact",
      "viewOfficerStation"
    ].forEach((id) => {
      document.getElementById(id).value = "";
    });
  }

  function resetCloseFirSection() {
    document.getElementById("closeFirId").value = "";
    document.getElementById("closeFirIdError").textContent = "";
    document.getElementById("closeFirSuccess").textContent = "";
    document.getElementById("closeAlreadyMessage").textContent = "";
    document.getElementById("closeFirBtn").disabled = true;
    document.getElementById("closeFirHomeBtn").classList.add("hidden");
    document.getElementById("closeFirDetailsBlock").classList.add("hidden");
    [
      "closeFirNumber",
      "closeDateFiled",
      "closeDescription",
      "closePlace",
      "closeStatus",
      "closeCompName",
      "closeCompContact"
    ].forEach((id) => {
      document.getElementById(id).value = "";
    });
  }

  function fillViewFirDetails(fir) {
    document.getElementById("viewFirNumber").value = fir.firNumber;
    document.getElementById("viewDateFiled").value = fir.dateFiled;
    document.getElementById("viewTimeFiled").value = fir.timeFiled;
    document.getElementById("viewPlace").value = fir.place;
    document.getElementById("viewStatus").value = fir.status;
    document.getElementById("viewDescription").value = fir.description;

    document.getElementById("viewCompName").value = fir.complainant.name;
    document.getElementById("viewCompAge").value = fir.complainant.age;
    document.getElementById("viewCompGender").value = fir.complainant.gender;
    document.getElementById("viewCompAddress").value = fir.complainant.address;
    document.getElementById("viewCompContact").value = fir.complainant.contact;
    document.getElementById("viewCompIdProof").value = fir.complainant.idProof;

    document.getElementById("viewOfficerName").value = fir.officer.name;
    document.getElementById("viewOfficerRank").value = fir.officer.rank;
    document.getElementById("viewOfficerBadge").value = fir.officer.badgeNumber;
    document.getElementById("viewOfficerContact").value = fir.officer.contactNumber;
    document.getElementById("viewOfficerStation").value = fir.officer.stationId;
  }

  function fillCloseFirDetails(fir) {
    document.getElementById("closeFirNumber").value = fir.firNumber;
    document.getElementById("closeDateFiled").value = fir.dateFiled;
    document.getElementById("closeDescription").value = fir.description;
    document.getElementById("closePlace").value = fir.place;
    document.getElementById("closeStatus").value = fir.status;
    document.getElementById("closeCompName").value = fir.complainant.name;
    document.getElementById("closeCompContact").value = fir.complainant.contact;

    const alreadyClosed = fir.status === "Closed";
    document.getElementById("closeAlreadyMessage").textContent = alreadyClosed
      ? "This FIR is already closed."
      : "";
    document.getElementById("closeFirBtn").disabled = alreadyClosed;
  }

  function bindQuickActions() {
    document.querySelectorAll("[data-action]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const action = btn.getAttribute("data-action");
        if (action === "add-officer") {
          resetAddOfficerForm();
          showSection("addOfficer");
        }
        if (action === "remove-officer") {
          refreshRemoveOfficerDropdown();
          resetRemoveOfficerSection();
          showSection("removeOfficer");
        }
        if (action === "view-fir") {
          resetViewFirSection();
          showSection("viewFir");
        }
        if (action === "close-fir") {
          refreshCloseFirDropdown();
          resetCloseFirSection();
          showSection("closeFir");
        }
      });
    });

    document.querySelectorAll(".js-back-home").forEach((btn) => {
      btn.addEventListener("click", () => {
        showSection("home");
      });
    });
  }

  function bindAddOfficerHandlers() {
    const form = document.getElementById("addOfficerForm");
    const success = document.getElementById("addOfficerSuccess");

    document.getElementById("addOfficerResetBtn").addEventListener("click", () => {
      resetAddOfficerForm();
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      clearFieldErrors("addOfficerForm");
      success.textContent = "";

      const officerName = document.getElementById("officerName").value.trim();
      const rank = document.getElementById("officerRank").value.trim();
      const badge = document.getElementById("officerBadge").value.trim();
      const contact = document.getElementById("officerContact").value.trim();

      let valid = true;

      if (officerName.length < 3) {
        document.getElementById("officerNameError").textContent = "Officer name must be at least 3 characters.";
        valid = false;
      }
      if (!rank) {
        document.getElementById("officerRankError").textContent = "Rank is required.";
        valid = false;
      }
      if (!/^[A-Za-z0-9]+$/.test(badge)) {
        document.getElementById("officerBadgeError").textContent = "Badge number must be alphanumeric.";
        valid = false;
      } else {
        const exists = state.officers.some((item) => item.badgeNumber.toLowerCase() === badge.toLowerCase());
        if (exists) {
          document.getElementById("officerBadgeError").textContent = "Badge number must be unique.";
          valid = false;
        }
      }
      if (!/^\d{10}$/.test(contact)) {
        document.getElementById("officerContactError").textContent = "Contact number must be exactly 10 digits.";
        valid = false;
      }

      if (!valid) {
        return;
      }

      const newOfficer = {
        officerId: document.getElementById("addOfficerId").value,
        name: officerName,
        rank,
        badgeNumber: badge,
        contactNumber: contact,
        stationId: state.stationId
      };

      // Backend integration: replace local push with API call to create officer in database.
      state.officers.push(newOfficer);
      refreshRemoveOfficerDropdown();
      success.textContent = "Officer added successfully.";

      // Backend integration: trigger officer list refresh endpoint for Admin tables when available.
      setTimeout(() => {
        resetAddOfficerForm();
        showSection("home");
      }, 1000);
    });
  }

  function bindRemoveOfficerHandlers() {
    const select = document.getElementById("removeOfficerId");
    const details = document.getElementById("removeOfficerDetailsBlock");
    const deleteBtn = document.getElementById("deleteOfficerBtn");
    const success = document.getElementById("removeOfficerSuccess");
    const homeBtn = document.getElementById("removeOfficerHomeBtn");

    select.addEventListener("change", () => {
      success.textContent = "";
      homeBtn.classList.add("hidden");
      const officerId = select.value;

      if (!officerId) {
        details.classList.add("hidden");
        deleteBtn.disabled = true;
        return;
      }

      const officer = state.officers.find((item) => item.officerId === officerId);
      if (!officer) {
        details.classList.add("hidden");
        deleteBtn.disabled = true;
        return;
      }

      details.classList.remove("hidden");
      deleteBtn.disabled = false;
      document.getElementById("removeOfficerName").value = officer.name;
      document.getElementById("removeOfficerRank").value = officer.rank;
      document.getElementById("removeOfficerBadge").value = officer.badgeNumber;
      document.getElementById("removeOfficerContact").value = officer.contactNumber;
      document.getElementById("removeOfficerStationId").value = officer.stationId;
    });

    deleteBtn.addEventListener("click", () => {
      if (!select.value) {
        document.getElementById("removeOfficerIdError").textContent = "Officer ID is required.";
        return;
      }

      showConfirm("Are you sure you want to delete this officer?", () => {
        const officerId = select.value;
        // Backend integration: replace local delete with API call to remove officer from database.
        state.officers = state.officers.filter((item) => item.officerId !== officerId);

        refreshRemoveOfficerDropdown();
        resetRemoveOfficerSection();
        success.textContent = "Officer successfully deleted.";
        homeBtn.classList.remove("hidden");
      });
    });

    homeBtn.addEventListener("click", () => {
      showSection("home");
    });
  }

  function bindViewFirHandlers() {
    const searchInput = document.getElementById("viewFirSearchInput");
    const searchBtn = document.getElementById("viewFirSearchBtn");
    const clearBtn = document.getElementById("viewFirClearBtn");
    const searchAnotherBtn = document.getElementById("viewFirSearchAnotherBtn");
    const error = document.getElementById("viewFirError");
    const resultBlock = document.getElementById("viewFirResultBlock");

    function performSearch() {
      const firId = searchInput.value.trim().toUpperCase();
      error.textContent = "";
      resultBlock.classList.add("hidden");

      if (!firId) {
        error.textContent = "Enter FIR ID.";
        return;
      }

      const fir = state.firs.find((item) => item.firId.toUpperCase() === firId);
      if (!fir) {
        error.textContent = "No FIR found with this ID";
        return;
      }

      fillViewFirDetails(fir);
      resultBlock.classList.remove("hidden");
    }

    searchBtn.addEventListener("click", performSearch);
    clearBtn.addEventListener("click", resetViewFirSection);
    searchAnotherBtn.addEventListener("click", resetViewFirSection);
  }

  function bindCloseFirHandlers() {
    const select = document.getElementById("closeFirId");
    const details = document.getElementById("closeFirDetailsBlock");
    const closeBtn = document.getElementById("closeFirBtn");
    const success = document.getElementById("closeFirSuccess");
    const backHomeBtn = document.getElementById("closeFirHomeBtn");

    select.addEventListener("change", () => {
      success.textContent = "";
      backHomeBtn.classList.add("hidden");
      const firId = select.value;

      if (!firId) {
        details.classList.add("hidden");
        closeBtn.disabled = true;
        return;
      }

      const fir = state.firs.find((item) => item.firId === firId);
      if (!fir) {
        details.classList.add("hidden");
        closeBtn.disabled = true;
        return;
      }

      details.classList.remove("hidden");
      fillCloseFirDetails(fir);
    });

    closeBtn.addEventListener("click", () => {
      const firId = select.value;
      if (!firId) {
        document.getElementById("closeFirIdError").textContent = "FIR ID is required.";
        return;
      }

      showConfirm("Are you sure you want to close this FIR?", () => {
        const fir = state.firs.find((item) => item.firId === firId);
        if (!fir || fir.status === "Closed") {
          return;
        }

        // Backend integration: replace local status update with API call to close FIR in database.
        fir.status = "Closed";
        fillCloseFirDetails(fir);
        refreshStats();
        refreshCloseFirDropdown();

        // Backend integration: refresh FIR list/table endpoint after close action.
        success.textContent = "FIR successfully closed.";
        backHomeBtn.classList.remove("hidden");
      });
    });

    backHomeBtn.addEventListener("click", () => {
      showSection("home");
    });
  }

  function bindModalHandlers() {
    confirmYesBtn.addEventListener("click", () => {
      if (typeof state.pendingConfirmAction === "function") {
        state.pendingConfirmAction();
      }
      closeConfirm();
    });

    confirmNoBtn.addEventListener("click", closeConfirm);
  }

  function init() {
    populateHeaderContext();
    refreshStats();
    refreshRemoveOfficerDropdown();
    refreshCloseFirDropdown();
    resetAddOfficerForm();
    resetRemoveOfficerSection();
    resetViewFirSection();
    resetCloseFirSection();
    bindQuickActions();
    bindAddOfficerHandlers();
    bindRemoveOfficerHandlers();
    bindViewFirHandlers();
    bindCloseFirHandlers();
    bindModalHandlers();
    showSection("home");
  }

  init();
})();
