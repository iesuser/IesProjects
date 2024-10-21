function changeRole(userId) {
    const changeRoleModal = new bootstrap.Modal(document.getElementById('changeRoleModal'));
    changeRoleModal.show();

    // Handle role changes on form submission
    const form = document.getElementById('changeRoleForm');
    form.onsubmit = function (event) {
        event.preventDefault();
        const newRole = document.getElementById('roleSelect').value;
        console.log(`User ID: ${userId}, New Role: ${newRole}`);
        // Call API to update role here
        changeRoleModal.hide();
    };
}