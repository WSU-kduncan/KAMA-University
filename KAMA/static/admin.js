document.addEventListener("DOMContentLoaded", () => {
    const panel = document.getElementById("adminInfo");
    const menuIcon = document.getElementById("menu-toggle");
    const closeBtn = document.getElementById("closeAdminInfo");

    if (menuIcon) {
        menuIcon.addEventListener("click", () => {
            panel.classList.add("open");
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            panel.classList.remove("open");
        });
    }
});
