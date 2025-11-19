document.addEventListener("DOMContentLoaded", () => {

    /* ========== ADVISOR INFO PANEL ========== */
    const menuToggle = document.querySelector(".menu-icon");
    const advisorInfo = document.getElementById("advisorInfo");
    const closeBtn = document.getElementById("closeAdvisorInfo");

    if (menuToggle && advisorInfo && closeBtn) {

        // Open sidebar when menu icon is clicked
        menuToggle.addEventListener("click", () => {
            advisorInfo.classList.add("open");
        });

        // Close panel when "Close" is pressed
        closeBtn.addEventListener("click", () => {
            advisorInfo.classList.remove("open");
        });
    }
});

