(function () {
  const storage = {
    firs: "fms_firs",
    complainants: "fms_complainants"
  };

  const state = {
    firs: [],
    complainants: [],
    currentUpdateFirId: null
  };

  const sections = {
    home: document.getElementById("homeSection"),
    registerFir: document.getElementById("registerFirSection"),
    updateFir: document.getElementById("updateFirSection"),
    searchFir: document.getElementById("searchFirSection"),
    registerComplainant: document.getElementById("registerComplainantSection")
  };

  function getUserContext() {
    return {
      officerId: localStorage.getItem("officer_id") || "OFC102",
      stationId: localStorage.getItem("station_id") || "STN01",
      officerName: localStorage.getItem("officer_name") || "A. Sharma",
      stationName: localStorage.getItem("station_name") || "Central Station"
    };
  }

  function readData(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : [];
    } catch (error) {
      return [];
    }
  }

  function writeData(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  function formatDate(date) {
    const d = String(date.getDate()).padStart(2, "0");
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const y = date.getFullYear();
    return d + "-" + m + "-" + y;
  }

  function formatTime(date) {
    let hours = date.getHours();
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const suffix = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    hours = hours ? hours : 12;
    return String(hours).padStart(2, "0") + ":" + minutes + " " + suffix;
  }

  function generateFirId() {
    const next = state.firs.length + 1;
    return "F" + String(next).padStart(2, "0");
  }

  function generateComplainantId() {
    const next = state.complainants.length + 1;
    return "C" + String(next).padStart(3, "0");
  }

  function showSection(name) {
    Object.keys(sections).forEach(function (key) {
      if (sections[key]) {
        sections[key].classList.toggle("hidden", key !== name);
      }
    });
  }

  function clearText(id) {
    const el = document.getElementById(id);
    if (el) el.textContent = "";
  }

  function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  function setValue(id, value) {
    const el = document.getElementById(id);
    if (el) el.value = value;
  }

  function setStats() {
    const total = state.firs.length;
    const active = state.firs.filter(function (item) {
      return item.status === "Registered" || item.status === "Under Investigation";
    }).length;
    const closed = state.firs.filter(function (item) {
      return item.status === "Closed";
    }).length;
    const pending = state.firs.filter(function (item) {
      return item.status === "Pending Review";
    }).length;

    setText("statTotalFirs", String(total));
    setText("statActiveCases", String(active));
    setText("statClosedCases", String(closed));
    setText("statPendingCases", String(pending));
  }

  function populateComplainantDropdowns() {
    const dropdown = document.getElementById("complainantId");
    if (dropdown) {
      dropdown.innerHTML = '<option value="">Select Complainant ID</option>';
      state.complainants.forEach(function (comp) {
        const option = document.createElement("option");
        option.value = comp.id;
        option.textContent = comp.id + " - " + comp.name;
        dropdown.appendChild(option);
      });
    }
  }

  function populateFirDropdown() {
    const dropdown = document.getElementById("updateFirId");
    if (!dropdown) return;
    dropdown.innerHTML = '<option value="">Select FIR ID</option>';
    state.firs.forEach(function (fir) {
      const option = document.createElement("option");
      option.value = fir.firId;
      option.textContent = fir.firId;
      dropdown.appendChild(option);
    });
  }

  function seedDefaultsIfEmpty() {
    if (!state.complainants.length) {
      state.complainants = [
        {
          id: "C001",
          name: "Rajesh Kumar",
          age: 34,
          gender: "Male",
          address: "45 Civil Lines, Delhi",
          contact: "9876543210",
          idProof: "Aadhaar"
        },
        {
          id: "C002",
          name: "Anita Sharma",
          age: 29,
          gender: "Female",
          address: "22 Green Park, Delhi",
          contact: "9123456780",
          idProof: "PAN Card"
        }
      ];
      writeData(storage.complainants, state.complainants);
    }
  }

  function fillRegisterFirSystemFields() {
    const now = new Date();
    const user = getUserContext();
    setValue("firId", generateFirId());
    setValue("firNumber", String(state.firs.length + 1));
    setValue("officerIdField", user.officerId);
    setValue("stationIdField", user.stationId);
    setValue("dateFiled", formatDate(now));
    setValue("timeFiled", formatTime(now));
    setValue("statusField", "Registered");
    setText("rfOfficerName", user.officerName);
    setText("rfStationName", user.stationName);
  }

  function fillRegisterComplainantSystemField() {
    setValue("complainantSystemId", generateComplainantId());
  }

  function clearErrors(ids) {
    ids.forEach(clearText);
  }

  function initQuickActions() {
    const buttons = document.querySelectorAll("[data-action]");
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        const action = button.getAttribute("data-action");
        if (action === "register-fir") {
          fillRegisterFirSystemFields();
          clearRegisterFirMessages();
          showSection("registerFir");
        } else if (action === "update-fir") {
          resetUpdateSection();
          showSection("updateFir");
        } else if (action === "search-fir") {
          resetSearchSection();
          showSection("searchFir");
        } else if (action === "register-complainant") {
          fillRegisterComplainantSystemField();
          clearRegisterComplainantMessages();
          showSection("registerComplainant");
        }
      });
    });

    document.querySelectorAll(".js-back-home").forEach(function (button) {
      button.addEventListener("click", function () {
        showSection("home");
      });
    });
  }

  function clearRegisterFirMessages() {
    clearErrors(["placeOccurrenceError", "complainantIdError", "firDescriptionError", "registerFirSuccess"]);
  }

  function clearRegisterComplainantMessages() {
    clearErrors([
      "compNameError",
      "compAgeError",
      "compGenderError",
      "compContactError",
      "compIdProofError",
      "compAddressError",
      "registerComplainantSuccess"
    ]);
  }

  function initRegisterFir() {
    const form = document.getElementById("registerFirForm");
    const resetBtn = document.getElementById("registerFirResetBtn");
    const desc = document.getElementById("firDescription");

    if (desc) {
      desc.addEventListener("input", function () {
        setText("firDescCounter", String(desc.value.length) + " characters");
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        setValue("placeOccurrence", "");
        setValue("firDescription", "");
        setValue("complainantId", "");
        setText("firDescCounter", "0 characters");
        clearRegisterFirMessages();
      });
    }

    if (!form) return;

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearRegisterFirMessages();

      const place = (document.getElementById("placeOccurrence").value || "").trim();
      const description = (document.getElementById("firDescription").value || "").trim();
      const complainantId = document.getElementById("complainantId").value;

      let valid = true;

      if (!place) {
        setText("placeOccurrenceError", "Place of occurrence is required.");
        valid = false;
      }
      if (!description) {
        setText("firDescriptionError", "Description is required.");
        valid = false;
      }
      if (!complainantId) {
        setText("complainantIdError", "Complainant ID is required.");
        valid = false;
      }

      if (!valid) return;

      const fir = {
        firId: document.getElementById("firId").value,
        firNumber: document.getElementById("firNumber").value,
        officerId: document.getElementById("officerIdField").value,
        stationId: document.getElementById("stationIdField").value,
        dateFiled: document.getElementById("dateFiled").value,
        timeFiled: document.getElementById("timeFiled").value,
        status: document.getElementById("statusField").value,
        placeOfOccurrence: place,
        description: description,
        complainantId: complainantId,
        officerName: getUserContext().officerName,
        officerRank: localStorage.getItem("officer_rank") || "Sub Inspector",
        badgeNumber: localStorage.getItem("officer_badge") || "B-102",
        officerContact: localStorage.getItem("officer_contact") || "9000000000"
      };

      state.firs.push(fir);
      writeData(storage.firs, state.firs);
      setStats();
      populateFirDropdown();

      setText("registerFirSuccess", "FIR registered successfully.");
      setValue("placeOccurrence", "");
      setValue("firDescription", "");
      setValue("complainantId", "");
      setText("firDescCounter", "0 characters");
      fillRegisterFirSystemFields();
    });
  }

  function initRegisterComplainant() {
    const form = document.getElementById("registerComplainantForm");
    const resetBtn = document.getElementById("registerComplainantResetBtn");

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        setValue("compName", "");
        setValue("compAge", "");
        setValue("compGender", "");
        setValue("compAddress", "");
        setValue("compContact", "");
        setValue("compIdProof", "");
        clearRegisterComplainantMessages();
      });
    }

    if (!form) return;

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearRegisterComplainantMessages();

      const name = (document.getElementById("compName").value || "").trim();
      const age = Number(document.getElementById("compAge").value);
      const gender = document.getElementById("compGender").value;
      const address = (document.getElementById("compAddress").value || "").trim();
      const contact = (document.getElementById("compContact").value || "").trim();
      const idProof = document.getElementById("compIdProof").value;

      let valid = true;
      if (!name) {
        setText("compNameError", "Name is required.");
        valid = false;
      }
      if (!Number.isInteger(age) || age <= 0) {
        setText("compAgeError", "Age must be greater than 0.");
        valid = false;
      }
      if (!gender) {
        setText("compGenderError", "Please select gender.");
        valid = false;
      }
      if (!address) {
        setText("compAddressError", "Address is required.");
        valid = false;
      }
      if (!/^\d{10}$/.test(contact)) {
        setText("compContactError", "Please enter a valid 10-digit contact number.");
        valid = false;
      }
      if (!idProof) {
        setText("compIdProofError", "Please select ID proof.");
        valid = false;
      }

      if (!valid) return;

      state.complainants.push({
        id: document.getElementById("complainantSystemId").value,
        name: name,
        age: age,
        gender: gender,
        address: address,
        contact: contact,
        idProof: idProof
      });
      writeData(storage.complainants, state.complainants);
      populateComplainantDropdowns();

      setText("registerComplainantSuccess", "Complainant registered successfully.");
      setValue("compName", "");
      setValue("compAge", "");
      setValue("compGender", "");
      setValue("compAddress", "");
      setValue("compContact", "");
      setValue("compIdProof", "");
      fillRegisterComplainantSystemField();
    });
  }

  function setUpdateFieldState(checkId, fieldId) {
    const checkbox = document.getElementById(checkId);
    const field = document.getElementById(fieldId);
    if (!checkbox || !field) return;
    const toggle = function () {
      field.disabled = !checkbox.checked;
      if (!checkbox.checked) field.value = "";
    };
    checkbox.addEventListener("change", toggle);
    toggle();
  }

  function bindUpdateSelection() {
    setUpdateFieldState("chkStatus", "newStatus");
    setUpdateFieldState("chkPlace", "newPlace");
    setUpdateFieldState("chkDescription", "newDescription");
  }

  function clearUpdateMessages() {
    clearErrors([
      "updateFirIdError",
      "newStatusError",
      "newPlaceError",
      "newDescriptionError",
      "updateSelectionError",
      "updateFirSuccess"
    ]);
  }

  function clearUpdateDetailFields() {
    [
      "udFirId",
      "udFirNumber",
      "udDateFiled",
      "udTimeFiled",
      "udOfficerId",
      "udStationId",
      "udComplainantId",
      "udStatus",
      "udPlace",
      "udDescription"
    ].forEach(function (id) {
      setValue(id, "");
    });
  }

  function fillUpdateDetails(fir) {
    if (!fir) {
      clearUpdateDetailFields();
      return;
    }

    setValue("udFirId", fir.firId);
    setValue("udFirNumber", fir.firNumber);
    setValue("udDateFiled", fir.dateFiled);
    setValue("udTimeFiled", fir.timeFiled);
    setValue("udOfficerId", fir.officerId);
    setValue("udStationId", fir.stationId);
    setValue("udComplainantId", fir.complainantId);
    setValue("udStatus", fir.status);
    setValue("udPlace", fir.placeOfOccurrence);
    setValue("udDescription", fir.description);
  }

  function resetUpdateSection() {
    clearUpdateMessages();
    setValue("updateFirId", "");
    state.currentUpdateFirId = null;
    fillUpdateDetails(null);
    setValue("newStatus", "");
    setValue("newPlace", "");
    setValue("newDescription", "");
    ["chkStatus", "chkPlace", "chkDescription"].forEach(function (id) {
      const checkbox = document.getElementById(id);
      if (checkbox) checkbox.checked = false;
      const field = id === "chkStatus" ? "newStatus" : id === "chkPlace" ? "newPlace" : "newDescription";
      const input = document.getElementById(field);
      if (input) input.disabled = true;
    });
  }

  function initUpdateFir() {
    const dropdown = document.getElementById("updateFirId");
    const updateBtn = document.getElementById("updateFirBtn");
    const modal = document.getElementById("confirmModal");
    const confirmBtn = document.getElementById("confirmUpdateBtn");
    const cancelBtn = document.getElementById("cancelUpdateBtn");

    bindUpdateSelection();

    if (dropdown) {
      dropdown.addEventListener("change", function () {
        clearUpdateMessages();
        const fir = state.firs.find(function (item) {
          return item.firId === dropdown.value;
        });
        state.currentUpdateFirId = fir ? fir.firId : null;
        fillUpdateDetails(fir || null);
      });
    }

    if (cancelBtn && modal) {
      cancelBtn.addEventListener("click", function () {
        modal.classList.add("hidden");
      });
    }

    if (updateBtn && modal) {
      updateBtn.addEventListener("click", function () {
        clearUpdateMessages();
        const selectedId = document.getElementById("updateFirId").value;
        const chkStatus = document.getElementById("chkStatus").checked;
        const chkPlace = document.getElementById("chkPlace").checked;
        const chkDescription = document.getElementById("chkDescription").checked;
        const newStatus = document.getElementById("newStatus").value;
        const newPlace = (document.getElementById("newPlace").value || "").trim();
        const newDescription = (document.getElementById("newDescription").value || "").trim();

        let valid = true;

        if (!selectedId) {
          setText("updateFirIdError", "Please select FIR ID.");
          valid = false;
        }
        if (!chkStatus && !chkPlace && !chkDescription) {
          setText("updateSelectionError", "Please select at least one field to update.");
          valid = false;
        }
        if (chkStatus && !newStatus) {
          setText("newStatusError", "Please select status.");
          valid = false;
        }
        if (chkPlace && !newPlace) {
          setText("newPlaceError", "Please enter place of occurrence.");
          valid = false;
        }
        if (chkDescription && !newDescription) {
          setText("newDescriptionError", "Please enter description.");
          valid = false;
        }

        if (!valid) return;

        modal.classList.remove("hidden");
      });
    }

    if (confirmBtn && modal) {
      confirmBtn.addEventListener("click", function () {
        const selectedId = document.getElementById("updateFirId").value;
        const index = state.firs.findIndex(function (item) {
          return item.firId === selectedId;
        });
        if (index < 0) {
          modal.classList.add("hidden");
          return;
        }

        if (document.getElementById("chkStatus").checked) {
          state.firs[index].status = document.getElementById("newStatus").value;
        }
        if (document.getElementById("chkPlace").checked) {
          state.firs[index].placeOfOccurrence = document.getElementById("newPlace").value.trim();
        }
        if (document.getElementById("chkDescription").checked) {
          state.firs[index].description = document.getElementById("newDescription").value.trim();
        }

        writeData(storage.firs, state.firs);
        setStats();
        fillUpdateDetails(state.firs[index]);
        setText("updateFirSuccess", "FIR updated successfully.");
        modal.classList.add("hidden");

        ["chkStatus", "chkPlace", "chkDescription"].forEach(function (id) {
          const checkbox = document.getElementById(id);
          if (checkbox) checkbox.checked = false;
        });
        setValue("newStatus", "");
        setValue("newPlace", "");
        setValue("newDescription", "");
        document.getElementById("newStatus").disabled = true;
        document.getElementById("newPlace").disabled = true;
        document.getElementById("newDescription").disabled = true;
      });
    }
  }

  function resetSearchSection() {
    setValue("searchFirId", "");
    clearErrors(["searchFirIdError", "searchError"]);
    document.getElementById("searchResultBlock").classList.add("hidden");
  }

  function populateSearchResult(fir) {
    const complainant = state.complainants.find(function (item) {
      return item.id === fir.complainantId;
    });

    setValue("sfFirNumber", fir.firNumber);
    setValue("sfDateFiled", fir.dateFiled);
    setValue("sfTimeFiled", fir.timeFiled);
    setValue("sfPlace", fir.placeOfOccurrence);
    setValue("sfDescription", fir.description);
    setValue("sfStatus", fir.status);

    setValue("sfCompName", complainant ? complainant.name : "N/A");
    setValue("sfCompAge", complainant ? String(complainant.age) : "N/A");
    setValue("sfCompGender", complainant ? complainant.gender : "N/A");
    setValue("sfCompAddress", complainant ? complainant.address : "N/A");
    setValue("sfCompContact", complainant ? complainant.contact : "N/A");
    setValue("sfCompIdProof", complainant ? complainant.idProof : "N/A");

    setValue("sfOfficerName", fir.officerName || "N/A");
    setValue("sfOfficerRank", fir.officerRank || "N/A");
    setValue("sfOfficerBadge", fir.badgeNumber || "N/A");
    setValue("sfOfficerContact", fir.officerContact || "N/A");
    setValue("sfOfficerStation", fir.stationId || "N/A");
  }

  function initSearchFir() {
    const searchBtn = document.getElementById("searchFirBtn");
    const clearBtn = document.getElementById("clearSearchBtn");
    const searchAnotherBtn = document.getElementById("searchAnotherBtn");

    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        resetSearchSection();
      });
    }

    if (searchAnotherBtn) {
      searchAnotherBtn.addEventListener("click", function () {
        resetSearchSection();
      });
    }

    if (!searchBtn) return;

    searchBtn.addEventListener("click", function () {
      clearErrors(["searchFirIdError", "searchError"]);
      document.getElementById("searchResultBlock").classList.add("hidden");

      const value = (document.getElementById("searchFirId").value || "").trim().toUpperCase();
      if (!value) {
        setText("searchFirIdError", "Please enter FIR ID.");
        return;
      }

      const fir = state.firs.find(function (item) {
        return item.firId.toUpperCase() === value;
      });

      if (!fir) {
        setText("searchError", "No FIR found with this ID.");
        return;
      }

      populateSearchResult(fir);
      document.getElementById("searchResultBlock").classList.remove("hidden");
    });
  }

  function init() {
    state.firs = readData(storage.firs);
    state.complainants = readData(storage.complainants);

    seedDefaultsIfEmpty();
    populateComplainantDropdowns();
    populateFirDropdown();
    setStats();
    fillRegisterFirSystemFields();
    fillRegisterComplainantSystemField();

    initQuickActions();
    initRegisterFir();
    initRegisterComplainant();
    initUpdateFir();
    initSearchFir();

    showSection("home");
  }

  init();
})();
