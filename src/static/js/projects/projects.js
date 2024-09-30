fetch('/api/projects')
    .then(response => response.json())
    .then(data => {
        if (Array.isArray(data)) {
            const projectTableBody = document.getElementById('projectTableBody');
            data.forEach(project => {
                const row = `
                    <tr data-project-id="${project.id}">
                        <td>${project.projects_name}</td>
                        <td>${project.contract_number || '----'}</td>
                        <td>${project.start_time}</td>
                        <td>${project.end_time}</td>
                        <td>${project.contractor || '----'}</td>
                        <td>${project.proj_location}</td>
                        <td>${project.proj_latitude}</td>
                        <td>${project.proj_longitude}</td>
                        <td>${project.geological_study ? "Yes" : "No"}</td>
                        <td>${project.geophysical_study ? "Yes" : "No"}</td>
                        <td>${project.hazard_study ? "Yes" : "No"}</td>
                        <td>${project.geodetic_study ? "Yes" : "No"}</td>
                        <td>${project.other_study ? "Yes" : "No"}</td>
                        <td>
                            <a class="btn btn-sm btn-primary" href="/view_project/${project.id}">ნახვა</a>
                        </td>
                        <td>
                            <img src="/static/img/pen-solid.svg" alt="Edit" style="width: 20px; height: 20px; cursor: pointer;" onclick="openEditProjectModal(${project.id})">
                        </td>
                        <td>
                            <img src="/static/img/trash-solid.svg" alt="Delete" style="width: 20px; height: 20px; cursor: pointer;" onclick="openConfirmDeleteProjectModal(${project.id})">
                        </td>
                    </tr>
                `;
                projectTableBody.innerHTML += row;
            });
            // Update map markers with the filtered data
            updateMapMarkers(data);
        } else {
            console.error('Error fetching project data from server');
        }
    })
    .catch(error => {
        console.error('Error fetching project data:', error);
    });


// Send POST request for creating a new project
function createProjectForm(event) {
    event.preventDefault(); // Prevent default form submission

    const form = document.getElementById('addProjectForm');
    const formData = new FormData(form);

    // Retrieve JWT token
    const token = localStorage.getItem('access_token');

    // makeApiRequest is a utility function defined elsewhere
    makeApiRequest('/api/projects', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}` // Include JWT token in the Authorization header
        },
        body: formData
    })
    .then(data => {
        if (data.message) {
            showAlert('success', data.message);
            window.location.reload(); // Reload page after success
        }else if (data.error) {
            showAlert('danger', data.error || 'Error: გაუმართავი პროექტის შექმნა.');
            closeModal('createProjectModal');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to open the Edit Project Modal
function openEditProjectModal(projectId) {
    fetch(`/api/project/${projectId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editProjectName').value = data.projects_name;
            document.getElementById('editContractNumber').value = data.contract_number;
            document.getElementById('editStartTime').value = data.start_time;
            document.getElementById('editEndTime').value = data.end_time;
            document.getElementById('editContractor').value = data.contractor;
            document.getElementById('editProjLocation').value = data.proj_location;
            document.getElementById('editProjLatitude').value = data.proj_latitude;
            document.getElementById('editProjLongitude').value = data.proj_longitude;

            // Set the data-project-id attribute for form submission
            document.getElementById('editProjectForm').setAttribute('data-project-id', data.id);

            const editProjectModal = new bootstrap.Modal(document.getElementById('editProjectModal'));
            editProjectModal.show();
        })
        .catch(error => console.error('Error fetching project data:', error));
}

// Function to handle form submission for editing a project
function submitProjectForm(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(document.getElementById('editProjectForm'));
    const projectId = document.getElementById("editProjectForm").getAttribute("data-project-id");

    // Retrieve JWT token
    const token = localStorage.getItem('access_token');

    makeApiRequest(`/api/project/${projectId}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}` // Include JWT token in the Authorization header
        },
        body: formData
    })
    .then(data => {
        if (data.error) {
            showAlert('danger', data.error);
            closeModal('editProjectModal');
        } else if(data.message){
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to confirm and delete a project
let projectIdToDelete = null;

function openConfirmDeleteProjectModal(projectId) {
    projectIdToDelete = projectId; // Store the project ID to delete
    const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteProjectModal'));
    confirmDeleteModal.show();
}

document.getElementById('confirmDeleteProjectButton').addEventListener('click', function() {
    if (projectIdToDelete !== null) {
        const token = localStorage.getItem('access_token');

        makeApiRequest(`/api/project/${projectIdToDelete}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}` // Include JWT token in the Authorization header
            }
        })
        .then(data => {
            if (data.message) {
                showAlert('success', data.message);
                const row = document.querySelector(`tr[data-project-id="${projectIdToDelete}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                showAlert('danger', data.error || 'Error: გაუმართავი პროექტის წაშლა.');
            }
        })
        .catch(error => {
            console.error('Error deleting project:', error);
        })
        .finally(() => {
            closeModal('confirmDeleteProjectModal');
            projectIdToDelete = null; // Clear the project ID
        });
    }
});
