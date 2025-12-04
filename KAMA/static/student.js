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
  
    if (typeof scheduleData !== "undefined" && scheduleData && scheduleData.length > 0) {
  
        const scheduleBox = document.getElementById("scheduleDisplay");
        let index = 0;
  
        function renderSchedule() {
            const sem = scheduleData[index];
            semesterDisplay.textContent = sem.name;
  
            if (!sem.courses || sem.courses.length === 0) {
                scheduleBox.innerHTML = `<p>No courses in this semester.</p>`;
                return;
            }
  
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
  
        rightArrow.addEventListener("click", () => {
            if (index < scheduleData.length - 1) {
                index++;
                renderSchedule();
            }
        });
  
        leftArrow.addEventListener("click", () => {
            if (index > 0) {
                index--;
                renderSchedule();
            }
        });
  
        renderSchedule();
  
    } else {
        semesterDisplay.textContent = "No Schedule";
    }
  
    /* ============================================================
       PREFERENCES MODAL
    ============================================================ */

    const openPrefBtn = document.getElementById("open-pref-modal");
    const modal = document.getElementById("preferences-modal");
    const closeModalBtn = document.getElementById("close-pref-modal");
    const savePrefBtn = document.getElementById("save-pref-modal");

    if (openPrefBtn) {
        openPrefBtn.addEventListener("click", () => {
            modal.classList.remove("hidden");
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", () => {
            modal.classList.add("hidden");
        });
    }

    // Clicking outside modal closes it
    window.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.add("hidden");
    });

    // Save preferences (PATCHED WITH MAX CREDITS)
    if (savePrefBtn) {
        savePrefBtn.addEventListener("click", async () => {

            const summer = document.getElementById("modal-summer-select").value;
            const coops = parseInt(document.getElementById("modal-coop-input").value);
            const years = parseInt(document.getElementById("modal-years-input").value);
            const maxcredits = parseInt(document.getElementById("modal-maxcredits-input").value);

            // ---- VALIDATION ----
            if (years < 1 || years > 10) {
                alert("Years must be between 1 and 10.");
                return;
            }

            if (coops < 0 || coops > 3) {
                alert("Co-Ops must be between 0 and 3.");
                return;
            }

            if (maxcredits < 6 || maxcredits > 25) {
                alert("Max credit hours must be between 6 and 25.");
                return;
            }

            // ---- UPDATE SUMMER ----
            await fetch("/student/update_summer", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ summer })
            });

            // ---- UPDATE CO-OPS ----
            await fetch("/student/update_coops", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ coops })
            });

            // ---- UPDATE YEARS ----
            await fetch("/student/update_years", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ years })
            });

            // ---- UPDATE MAX CREDIT HOURS (NEW) ----
            await fetch("/student/update_maxcredits", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ maxcredits })
            });

            alert("Preferences saved! Please regenerate your schedule.");

            modal.classList.add("hidden");

            // Force user to regenerate schedule visually
            const scheduleBox = document.getElementById("scheduleDisplay");
            const semName = document.getElementById("semesterName");

            if (scheduleBox) scheduleBox.innerHTML = "<p>Preferences changed — please regenerate.</p>";
            if (semName) semName.textContent = "Pending…";

        });
    }


    /* ============================================================
       GENERATE SCHEDULE WITH POPUP ON FAILURE
    ============================================================ */

    const generateBtn = document.querySelector(".generate-btn");

    if (generateBtn) {
        generateBtn.addEventListener("click", async (e) => {
            e.preventDefault();

            const res = await fetch("/generate-schedule", {
                method: "POST"
            });

            if (!res.ok) {
                // Show failure popup
                document.getElementById("genFailModal").classList.remove("hidden");
                return;
            }

            // Success → reload dashboard
            location.reload();
        });
    }

    // Close popup
    const closeFail = document.getElementById("closeGenFail");
    if (closeFail) {
        closeFail.addEventListener("click", () => {
            document.getElementById("genFailModal").classList.add("hidden");
        });
    }

});
