document.addEventListener("DOMContentLoaded", () => {
  /* ====== INFO PANEL ====== */
  const menuToggle = document.getElementById("menu-toggle");
  const studentInfo = document.getElementById("studentInfo");
  const closeInfo = document.getElementById("closeInfo");

  if (menuToggle && studentInfo && closeInfo) {
    menuToggle.addEventListener("click", () => {
      studentInfo.classList.add("open");
    });

    closeInfo.addEventListener("click", () => {
      studentInfo.classList.remove("open");
    });
  }

  /* ====== SEMESTER SWITCHING ====== */
  const semesterDisplay = document.getElementById("semesterName");
  const leftArrow = document.querySelector(".left-arrow");
  const rightArrow = document.querySelector(".right-arrow");

  const includeSummer = typeof hasSummer !== "undefined" ? hasSummer : false;

  let startYear = 2026;
  let currentIndex = 0;

  const semesters = [];
  let year = startYear;
  const baseSequence = ["Fall", "Spring"];

  while (semesters.length < 8) {
    for (let term of baseSequence) {
      semesters.push(`${term} ${year}`);

      if (term === "Spring") {
        if (includeSummer && semesters.length < 8) {
          semesters.push(`Summer ${year}`);
        }
        year++; // advance year after Spring
      }

      if (semesters.length >= 8) break;
    }
  }

  function updateSemester() {
    semesterDisplay.textContent = semesters[currentIndex];
  }

  // Event listeners for navigation
  rightArrow.addEventListener("click", () => {
    if (currentIndex < semesters.length - 1) {
      currentIndex++;
      updateSemester();
    }
  });

  leftArrow.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateSemester();
    }
  });

  // Initialize the first display
  updateSemester();
});

