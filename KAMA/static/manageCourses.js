document.addEventListener("DOMContentLoaded", () => {

    // ================================
    // ELEMENTS
    // ================================
    const modal = document.getElementById("addCourseModal");
    const openBtn = document.getElementById("openAddCourseModal");
    const closeBtn = document.getElementById("closeModalBtn");
    const saveBtn = document.getElementById("saveCourseBtn");


    // ================================
    // OPEN MODAL
    // ================================
    openBtn.addEventListener("click", () => {
        modal.classList.remove("hidden");  // Show modal
    });


    // ================================
    // CLOSE MODAL
    // ================================
    closeBtn.addEventListener("click", () => {
        modal.classList.add("hidden");  // Hide modal
    });


    // ================================
    // ADD COURSE
    // ================================
    saveBtn.addEventListener("click", async () => {

        const id = document.getElementById("newCourseID").value.trim();
        const semester = document.getElementById("newCourseSemester").value.trim();
        const code = document.getElementById("newCourseCode").value.trim();
        const name = document.getElementById("newCourseName").value.trim();
        const credits = document.getElementById("newCourseCredits").value.trim();

        // Require all fields
        if (!id || !semester || !code || !name || !credits) {
            alert("All fields are required.");
            return;
        }

        const response = await fetch("/add-course", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                id,
                semester,
                code,
                name,
                credits
            })
        });

        const result = await response.json();

        if (result.success) {
            alert("Course added successfully!");
            window.location.reload();
        } else {
            alert("Error adding course. See console for details.");
            console.error(result.error);
        }
    });


    // ================================
    // DELETE COURSE
    // ================================
    document.querySelectorAll(".deleteCourseBtn").forEach(btn => {
        btn.addEventListener("click", async function() {

            const row = this.closest("tr");
            const courseID = row.dataset.courseId;

            if (!confirm("Are you sure you want to delete this course?")) {
                return;
            }

            const response = await fetch("/delete-course", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ course_id: courseID })
            });

            const result = await response.json();

            if (result.success) {
                alert("Course deleted!");
                window.location.reload();
            } else {
                alert("Error deleting course.");
                console.error(result.error);
            }
        });
    });

});
