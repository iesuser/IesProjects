// Function to open modal and populate form with role data
function populateEditRoleModal(roleId) {
    const token = localStorage.getItem('access_token');

    fetch(`/api/roles/${roleId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(role => {
        // Populate form fields
        document.getElementById('editRoleId').value = roleId;
        document.getElementById('editRoleName').value = role.name;
        document.getElementById('editIsAdmin').checked = role.is_admin;
        document.getElementById('editCanUsers').checked = role.can_users;
        document.getElementById('editCanProject').checked = role.can_project;
        document.getElementById('editCanGeophysic').checked = role.can_geophysic;
        document.getElementById('editCanGeologic').checked = role.can_geologic;
        document.getElementById('editCanHazard').checked = role.can_hazard;
        document.getElementById('editCanGeodetic').checked = role.can_geodetic;

        // Show the modal
        const editRoleModal = new bootstrap.Modal(document.getElementById('editRoleModal'));
        editRoleModal.show();
    })
    .catch(error => console.error('Error fetching role data:', error));
}

// Event listener for form submission
document.getElementById('editRoleForm').onsubmit = function (event) {
    event.preventDefault();
    submitEditRoleForm();
};

// Function to submit edited role data
function submitEditRoleForm() {
    const token = localStorage.getItem('access_token');
    const roleId = document.getElementById('editRoleId').value;
    const formData = new FormData(document.getElementById('editRoleForm'));

    const data = {
        name: formData.get('name'),
        is_admin: formData.get('is_admin') === 'on',
        can_users: formData.get('can_users') === 'on',
        can_project: formData.get('can_project') === 'on',
        can_geophysic: formData.get('can_geophysic') === 'on',
        can_geologic: formData.get('can_geologic') === 'on',
        can_hazard: formData.get('can_hazard') === 'on',
        can_geodetic: formData.get('can_geodetic') === 'on'
    };

    makeApiRequest(`/api/roles/${roleId}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(result => {
        if (result.message) {
            window.location.reload(); // Reload to reflect changes
        } else if (result.error) {
            showAlert('danger', result.error || 'როლის განახლების შეცდომა');
        }
    })
    .catch(error => console.error('Error updating role:', error));
}
