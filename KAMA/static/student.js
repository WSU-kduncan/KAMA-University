document.addEventListener("DOMContentLoaded", () => {

  /* ============================================================
     INFO PANEL
  ============================================================ */
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

  /* ============================================================
     REAL SCHEDULE DISPLAY
  ============================================================ */

  const semesterDisplay = document.getElementById("semesterName");
  const leftArrow = document.querySelector(".left-arrow");
  const rightArrow = document.querySelector(".right-arrow");

  // scheduleData is injected from student.html
  if (typeof scheduleData !== "undefined" && scheduleData && scheduleData.length > 0) {

      const scheduleBox = document.getElementById("scheduleDisplay");
      let index = 0;

      function renderSchedule() {
          const sem = scheduleData[index];

          // Semester title display
          semesterDisplay.textContent = sem.name;

          // No courses?
          if (!sem.courses || sem.courses.length === 0) {
              scheduleBox.innerHTML = `<p>No courses in this semester.</p>`;
              return;
          }

          // Render table
          scheduleBox.innerHTML = `
              <table class="schedule-table">
                  <thead>
                      <tr>
                          <th>Course Code</th>
                          <th>Course Name</th>
                          <th>Credits</th>
                      </tr>
                  </thead>
                  <tbody>
                      ${sem.courses.map(c => `
                          <tr>
                              <td>${c[0]}</td>
                              <td>${c[1]}</td>
                              <td>${c[2]}</td>
                          </tr>
                      `).join("")}
                  </tbody>
              </table>
          `;
      }

      // Next semester
      rightArrow.addEventListener("click", () => {
          if (index < scheduleData.length - 1) {
              index++;
              renderSchedule();
          }
      });

      // Previous semester
      leftArrow.addEventListener("click", () => {
          if (index > 0) {
              index--;
              renderSchedule();
          }
      });

      // Initial load
      renderSchedule();

  } else {
      // No schedule in DB
      semesterDisplay.textContent = "No Schedule";
  }

});
