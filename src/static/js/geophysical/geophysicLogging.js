document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicLoggingTableContainer = document.getElementById('geophysicLoggingTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    // Fetch data from API endpoint geophysic_logging
    fetch(`/api/geophysic_logging/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicLoggingTable = document.getElementById('geophysicLoggingTable');

                data.forEach(data => {
                    const archivalImgLink = data.archival_img ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/logging/archival_img/${data.archival_img}" target="_blank">${data.archival_img}</a>` : 
                    '---';

                    const archivalExcelLink = data.archival_excel ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/logging/archival_excel/${data.archival_excel}" target="_blank">${data.archival_excel}</a>` : 
                        '---';

                    const archivalPdfLink = data.archival_pdf ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/logging/archival_pdf/${data.archival_pdf}" target="_blank">${data.archival_pdf}</a>` : 
                    '---';

                    const row = `
                        <tr data-geophysicLogging-id="${data.id}">
                            <td>${data.longitude}</td>
                            <td>${data.latitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${archivalImgLink}</td>
                            <td>${archivalExcelLink}</td>
                            <td>${archivalPdfLink}</td>
                            <td>
                                <img src="/static/img/pen-solid.svg" alt="Edit" style="width: 20px; height: 20px; cursor: pointer;" onclick="openGeophysicLoggingModal(true, ${data.id})">
                            </td>
                            <td>
                                <img src="/static/img/trash-solid.svg" alt="Delete" style="width: 20px; height: 20px; cursor: pointer;" onclick="openConfirmDeleteGeophysicLoggingModal(${data.id})">
                            </td>
                        </tr>
                    `;
                    geophysicLoggingTable.innerHTML += row;
                });
            }else{
                // If data is not an array, hide the table
                geophysicLoggingTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});

// Function to confirm and delete a logging
let loggingIdDelete = null;

function openConfirmDeleteGeophysicLoggingModal(loggingId) {
    loggingIdDelete = loggingId; // Store the logging ID to delete
    const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteGeophysicLoggingModal'));
    confirmDeleteModal.show();
}

let geophysicLoggingId = null;

// Open the modal for creating or editing a GeophysicSeismic record
function openGeophysicLoggingModal(editMode = false, geophyLoggingId = null) {
    const modalTitle = document.getElementById('GeophysicLoggingModalTitle');
    const submitButton = document.getElementById('submitGeophysicLoggingBtn');
    const form = document.getElementById('GeophysicLoggingForm');
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    
    isEditMode = editMode;
    currentGeophysicalId = geophysicalId;
    geophysicLoggingId = geophyLoggingId;

    if (editMode) {
        modalTitle.textContent = "გეოფიზიკური კაროტაჟის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicLoggingData(currentGeophysicalId, geophysicLoggingId);
    } else {
        modalTitle.textContent = "გეოფიზიკური კაროტაჟის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicLoggingModal'));
    modal.show();
}

// Fetch data for editing a GeophysicLogging record
function fetchGeophysicLoggingData(geophysicalId, geophysicLoggingId) {
    fetch(`/api/geophysic_logging/${geophysicalId}/${geophysicLoggingId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('geophysicLoggingId').value = data.id;
                document.getElementById('logging_longitude').value = data.longitude;
                document.getElementById('logging_latitude').value = data.latitude;
                document.getElementById('logging_profile_length').value = data.profile_length;

            } else {
                showAlert('danger', 'გეოფიზიკური კაროტაჟი არ მოიძებნა.');
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function submitGeophysicLoggingForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicLoggingForm'));
    const url = isEditMode ? `/api/geophysic_logging/${currentGeophysicalId}/${geophysicLoggingId}` : `/api/geophysic_logging/${currentGeophysicalId}`;
    const method = isEditMode ? 'PUT' : 'POST';

    // Retrieve the JWT token from localStorage (or wherever you store it)
    const token = localStorage.getItem('access_token');

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
            showAlert('danger', data.error || 'Error: გაუმართავი გეოფიზიკური კაროტაჟის რედაქტირება/დამატება.');
            closeModal('GeophysicLoggingModal');
        } else if(data.message){
            window.location.reload(); // Reload the page to reflect changes
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('GeophysicLoggingForm').onsubmit = submitGeophysicLoggingForm;

document.getElementById('confirmDeleteGeophysicLoggingButton').addEventListener('click', function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");

    if (loggingIdDelete !== null) {
        const token = localStorage.getItem('access_token');
        
        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/geophysic_logging/${geophysicalId}/${loggingIdDelete}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        })
        .then(data => {
            if (data.message) {
                showAlert('success', data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-geophysicLogging-id="${loggingIdDelete}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                showAlert('danger', data.error || 'Error: გაუმართავი გეოფიზიკური კაროტაჟის წაშლა.');
            }
        })
        .catch(error => {
            console.error('Error deleting geophysicLogging:', error);
        })
        .finally(() => {
            closeModal('confirmDeleteGeophysicLoggingModal');
            loggingIdDelete = null; // Clear the seismic ID
        });
    }
});