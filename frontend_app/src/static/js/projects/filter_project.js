// Send POST request for filter project
function filterProjectForm(event) {
    event.preventDefault(); // Prevent default form submission

    const form = document.getElementById('filterProjectForm');
    const formData = new FormData(form);

    // Retrieve JWT token
    const token = sessionStorage.getItem('access_token');

    // makeApiRequest is a utility function defined elsewhere
    makeApiRequest('/api/filter_project', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}` // Include JWT token in the Authorization header
        },
        body: formData
    })
    .then(data => {
        if (Array.isArray(data)) {
            // Clear old project table data
            const projectTableBody = document.getElementById('projectTableBody');
            projectTableBody.innerHTML = ''; // Clear previous data

            // Append the new filtered data
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

}