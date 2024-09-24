document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    const geophysicalTableContainer = document.getElementById('geophysicalTableContainer');

    fetch(`/api/geophysical/${projectId}`)
    .then(response => response.json())
    .then(data => {
        // Check if data is an array
        if (Array.isArray(data)) {
            const geophysicalTableBody = document.getElementById('geophysicalTableBody');

            data.forEach(geophysical => {
                const archivalExcelLink = geophysical.archival_excel ? 
                `<a href="/${projectId}/geophysical/archival_excel/${geophysical.archival_excel}" target="_blank">${geophysical.archival_excel}</a>` : 
                '----';

                const archivalPdfLink = geophysical.archival_pdf ? 
                    `<a href="/${projectId}/geophysical/archival_pdf/${geophysical.archival_pdf}" target="_blank">${geophysical.archival_pdf}</a>` : 
                    '----';

                const row = `
                    <tr data-geophysical-id="${geophysical.id}">
                        <td>${geophysical.seismic_profiles ? "Yes" : "No"}</td>
                        <td>${geophysical.profiles_number}</td>
                        <td>${geophysical.vs30}</td>
                        <td>${geophysical.ground_category_geo}</td>
                        <td>${geophysical.ground_category_euro}</td>
                        <td>${geophysical.geophysical_logging ? "Yes" : "No"}</td>
                        <td>${geophysical.logging_number}</td>
                        <td>${geophysical.electrical_profiles ? "Yes" : "No"}</td>
                        <td>${geophysical.point_number}</td>
                        <td>${geophysical.georadar ? "Yes" : "No"}</td>
                        <td>${archivalExcelLink}</td>
                        <td>${archivalPdfLink}</td>
                        <td>
                            <a class="btn btn-sm btn-primary" href="/view_geophysical/${geophysical.id}">ნახვა</a>
                        </td>
                        <td>
                            <img src="/static/img/pen-solid.svg" alt="Edit" style="width: 20px; height: 20px; cursor: pointer;" onclick="openGeophysicalModal(true, ${geophysical.id})">
                        </td>
                        <td>
                            <img src="/static/img/trash-solid.svg" alt="Delete" style="width: 20px; height: 20px; cursor: pointer;" onclick="openConfirmDeleteGeophysicalModal(${projectId}, ${geophysical.id})">
                        </td>
                    </tr>
                `;
                geophysicalTableBody.innerHTML += row;
            });
        } else {
            // If data is not an array, hide the table
            geophysicalTableContainer.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        // Handle error scenario, e.g., show an error message on the UI
    });

});

// Function to confirm and delete a project
let projectIdToDelete = null;
let geophysicalIdDelete = null;

function openConfirmDeleteGeophysicalModal(projectId, geophysicalId) {
    projectIdToDelete = projectId; // Store the project ID to delete
    geophysicalIdDelete = geophysicalId;
    const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteGeophysicalModal'));
    confirmDeleteModal.show();
}

let isEditMode = false;
let currentProjectId = null;
let geophysicalId = null;

// Open the modal for creating or editing a Geophysical record
function openGeophysicalModal(editMode = false, geophyId = null) {
    const modalTitle = document.getElementById('GeophysicalModalTitle');
    const submitButton = document.getElementById('submitGeophysicalBtn');
    const form = document.getElementById('GeophysicalForm');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    isEditMode = editMode;
    currentProjectId = projectId;
    geophysicalId = geophyId;

    if (editMode) {
        modalTitle.textContent = "სეისმური პროფილის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicalData(currentProjectId, geophysicalId);
    } else {
        modalTitle.textContent = "სეისმური პროფილის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicalModal'));
    modal.show();
}

// Fetch data for editing a Geophysical record
function fetchGeophysicalData(projectId, geophysicalId) {
    // Fetch the existing data for the geophysical record
    fetch(`/api/geophysical/${projectId}/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                // Fill the form fields with existing data
                document.getElementById('geophysicalId').value = data.id;
                document.getElementById('vs30').value = data.vs30;
                document.getElementById('groundCategoryGeo').value = data.ground_category_geo;
                document.getElementById('groundCategoryEuro').value = data.ground_category_euro;

                // console.log(document.getElementById('vs30').value, data.vs30)
    
            } else {
                showAlert('danger', 'გეოფიზიკური კვლევა არ მოიძებნა.');
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function submitGeophysicalForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicalForm'));
    const url = isEditMode ? `/api/geophysical/${currentProjectId}/${geophysicalId}` : `/api/geophysical/${currentProjectId}`;
    const method = isEditMode ? 'PUT' : 'POST';

    // Retrieve the JWT token from sessionStorage (or wherever you store it)
    const token = sessionStorage.getItem('access_token');
    // makeApiRequest is in the globalAccessControl.js
    makeApiRequest(url, {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        },
        body: formData
    })
    .then(data => {
        if (data.error) {
            showAlert('danger', data.error || 'Error: გაუმართავი პროექტის რედაქტირება/დამატება.');
            closeModal('GeophysicalModal');
        } else if(data.message){
            window.location.reload(); // Reload the page to reflect changes
        } 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('GeophysicalForm').onsubmit = submitGeophysicalForm;

document.getElementById('confirmDeleteGeophysicalButton').addEventListener('click', function() {
    if (geophysicalIdDelete !== null && projectIdToDelete !== null) {
        const token = sessionStorage.getItem('access_token');

        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/geophysical/${projectIdToDelete}/${geophysicalIdDelete}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        })
        .then(data => {
            if (data.message) {
                showAlert('success', data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-geophysical-id="${geophysicalIdDelete}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                showAlert('danger', data.error || 'Error: გაუმართავი გეოფიზიკის წაშლა.');
            }
        })
        .catch(error => {
            console.error('Error deleting geophysical:', error);
        })
        .finally(() => {
            closeModal('confirmDeleteGeophysicalModal');
            geophysicalIdDelete = null; // Clear the project ID
        });
    }
});