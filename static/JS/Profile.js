function toggleEditMode() {
    const form = document.getElementById("profile-form");
    const inputs = form.querySelectorAll("input");
    const saveButton = document.getElementById("save-button");
    const editButton = document.getElementById("edit-button");

    const isEditing = saveButton.style.display === "inline-block";

    if (isEditing) {
        saveButton.style.display = "none";
        editButton.textContent = "Edit Profile";

        inputs.forEach(input => input.setAttribute("disabled", "true"));
    } else {
        saveButton.style.display = "inline-block";
        editButton.textContent = "Cancel Edit";

        inputs.forEach(input => input.removeAttribute("disabled"));
    }
}

document.getElementById("profile-form").addEventListener("submit", function(event) {
    event.preventDefault();

    this.submit();
    toggleEditMode();
});