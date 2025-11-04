document.addEventListener("DOMContentLoaded", () => {
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
});

