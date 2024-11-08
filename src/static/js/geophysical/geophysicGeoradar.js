document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicGeoradarTableContainer = document.getElementById('geophysicGeoradarTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    // Fetch data from API endpoint geophysic_logging
    fetch(`/api/geophysic_georadar/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicGeoradarTable = document.getElementById('geophysicGeoradarTable');

                data.forEach(data => {
                    const archivalImgLink = data.archival_img ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/georadar/archival_img/${data.archival_img}" target="_blank">${data.archival_img}</a>` : 
                    '---';

                    const archivalExcelLink = data.archival_excel ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/georadar/archival_excel/${data.archival_excel}" target="_blank">${data.archival_excel}</a>` : 
                        '---';

                    const archivalPdfLink = data.archival_pdf ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/georadar/archival_pdf/${data.archival_pdf}" target="_blank">${data.archival_pdf}</a>` : 
                    '---';

                    const row = `
                        <tr data-geophysicGeoradar-id="${data.id}">
                            <td>${data.latitude}</td>    
                            <td>${data.longitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${archivalImgLink}</td>
                            <td>${archivalExcelLink}</td>
                            <td>${archivalPdfLink}</td>
                            <td>
                                <img src="/static/img/pen-solid.svg" alt="Edit" style="width: 20px; height: 20px; cursor: pointer;" onclick="openGeophysicGeoradarModal(true, ${data.id})">
                            </td>
                            <td>
                                <img src="/static/img/trash-solid.svg" alt="Delete" style="width: 20px; height: 20px; cursor: pointer;" onclick="openConfirmDeleteGeophysicGeoradarModal(${data.id})">
                            </td>
                        </tr>
                    `;
                    geophysicGeoradarTable.innerHTML += row;
                });
            }else{
                // If data is not an array, hide the table
                geophysicGeoradarTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});

// Function to confirm and delete a georadar
let georadarIdDelete = null;

function openConfirmDeleteGeophysicGeoradarModal(georadarId) {
    georadarIdDelete = georadarId; // Store the georadar ID to delete
    const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteGeophysicGeoradarModal'));
    confirmDeleteModal.show();
}

let geophysicGeoradarId = null;

// Open the modal for creating or editing a GeophysicGeoradar record
function openGeophysicGeoradarModal(editMode = false, geophyGeoradarId = null) {
    const modalTitle = document.getElementById('GeophysicGeoradarModalTitle');
    const submitButton = document.getElementById('submitGeophysicGeoradarBtn');
    const form = document.getElementById('GeophysicGeoradarForm');
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    
    isEditMode = editMode;
    currentGeophysicalId = geophysicalId;
    geophysicGeoradarId = geophyGeoradarId;

    if (editMode) {
        modalTitle.textContent = "გეორადარის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicGeoradarData(currentGeophysicalId, geophysicGeoradarId);
    } else {
        modalTitle.textContent = "გეორადარის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicGeoradarModal'));
    modal.show();
}


// Fetch data for editing a geophysicGeoradar record
function fetchGeophysicGeoradarData(geophysicalId, geophysicGeoradarId) {
    fetch(`/api/geophysic_georadar/${geophysicalId}/${geophysicGeoradarId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('geophysicGeoradarId').value = data.id;
                document.getElementById('georadar_longitude').value = data.longitude;
                document.getElementById('georadar_latitude').value = data.latitude;
                document.getElementById('georadar_profile_length').value = data.profile_length;

            } else {
                alert('გეორადარის ჩანაწერი არ მოიძებნა.');
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function submitGeophysicGeoradarForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicGeoradarForm'));
    const url = isEditMode ? `/api/geophysic_georadar/${currentGeophysicalId}/${geophysicGeoradarId}` : `/api/geophysic_georadar/${currentGeophysicalId}`;
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
            showAlert('danger', data.error || 'Error: გაუმართავი გეორადარის რედაქტირება/დამატება.');
            closeModal('GeophysicGeoradarModal');
        } else if(data.message){
            window.location.reload(); // Reload the page to reflect changes
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('GeophysicGeoradarForm').onsubmit = submitGeophysicGeoradarForm;

document.getElementById('confirmDeleteGeophysicGeoradarButton').addEventListener('click', function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");

    if (georadarIdDelete !== null) {
        const token = localStorage.getItem('access_token');

        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/geophysic_georadar/${geophysicalId}/${georadarIdDelete}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        })
        .then(data => {
            if (data.message) {
                showAlert('success', data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-geophysicGeoradar-id="${georadarIdDelete}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                showAlert('danger', data.error || 'Error: გაუმართავი გეორადარის წაშლა.');
            }
        })
        .catch(error => {
            console.error('Error deleting geophysicGeoradar:', error);
        })
        .finally(() => {
            closeModal('confirmDeleteGeophysicGeoradarModal');
            georadarIdDelete = null; // Clear the georadar ID
        });
    }
});