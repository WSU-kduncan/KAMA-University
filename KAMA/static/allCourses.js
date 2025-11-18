function filterCourses() {
    const search = document.getElementById("searchInput").value.toLowerCase();
    const dept = document.getElementById("deptFilter").value;
    const sem = document.getElementById("semesterFilter").value;
    const cred = document.getElementById("creditFilter").value;

    const rows = document.querySelectorAll("table tr:not(:first-child)");

    rows.forEach(row => {
        const code = row.children[0].innerText.toLowerCase();
        const name = row.children[1].innerText.toLowerCase();
        const credits = row.children[2].innerText;
        const semester = row.children[3].innerText;

        let show = true;

        // Search filter
        if (search && !(code.includes(search) || name.includes(search))) {
            show = false;
        }

        // Department filter
        if (dept && !code.startsWith(dept.toLowerCase())) {
            show = false;
        }

        // Semester filter
        if (sem && !semester.includes(sem)) {
            show = false;
        }

        // Credit filter
        if (cred && credits !== cred) {
            show = false;
        }

        row.style.display = show ? "" : "none";
    });
}

// Attach event listeners when DOM is ready
window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("searchInput").addEventListener("input", filterCourses);
    document.getElementById("deptFilter").addEventListener("change", filterCourses);
    document.getElementById("semesterFilter").addEventListener("change", filterCourses);
    document.getElementById("creditFilter").addEventListener("change", filterCourses);
});
