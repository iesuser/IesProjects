document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    const geologicalTableContainer = document.getElementById('geologicalTableContainer');

    let permissions = getPermissions()

    let thEditGeologic = document.getElementById('thEditGeologic')
    let thDeleteGeologic = document.getElementById('thDeleteGeologic')

    if (!permissions.can_geophysic){
        thEditGeologic.remove()
        thDeleteGeologic.remove()
    }


    // Fetch data from API endpoint
    fetch(`/api/geological/${projectId}`)
        .then(response => response.json())
        .then(data => {
            // Check if data is an array
            if (Array.isArray(data)) {
                const geologicalTableBody = document.getElementById('geologicalTableBody');
                data.forEach(geological => {
                    const row = `
                        <tr>
                            <td>${geological.geological_survey ? "Yes" : "No"}</td>
                            <td>${geological.objects_number}</td>
                            <td>${geological.boreholes ? "Yes" : "No"}</td>
                            <td>${geological.boreholes_number}</td>
                            <td>${geological.pits ? "Yes" : "No"}</td>
                            <td>${geological.pits_number}</td>
                            <td>${geological.laboratory_tests ? "Yes" : "No"}</td>
                            <td>${geological.points_number}</td>
                            <td>${geological.archival_material}</td>
                            <td>
                            <a class="btn btn-sm btn-primary" href="/view_geophysical/${geological.id}">ნახვა</a>
                            </td>
                             ${permissions.can_geologic ? `<td><img src="/static/img/pen-solid.svg" alt="Edit" style="width: 20px; height: 20px; cursor: pointer;" onclick="openGeophysicalModal(true, ${geological.id})"></td>` : ''}

                             ${permissions.can_geologic ? `<td><img src="/static/img/trash-solid.svg" alt="Delete" style="width: 20px; height: 20px; cursor: pointer;" onclick="openConfirmDeleteGeophysicalModal(${projectId}, ${geological.id})"></td>` : ''}
                        </tr>
                    `;
                    geologicalTableBody.innerHTML += row;
                });
                // Add click event listener to each <tr> to navigate to detailed view
                const tableRows = geologicalTableBody.getElementsByTagName('tr');
                Array.from(tableRows).forEach(row => {
                    row.style.cursor = 'pointer';
                    row.addEventListener('click', function() {
                        const href = row.getAttribute('data-href');
                        if (href) {
                            window.location.href = href;
                        }
                    });
                });
            } else {
                // If data is not an array, hide the table
                geologicalTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});