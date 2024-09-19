document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    const geologicalTableContainer = document.getElementById('geologicalTableContainer');

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
                                <a class="btn btn-sm btn-primary" href="#">View</a>
                            </td>
                            <td>
                                <a class="btn btn-sm btn-info" href="#">Edit</a>
                            </td>
                            <td>
                                <form action="#" method="POST" style="display:inline;">
                                    <button type="submit" class="btn btn-sm btn-danger btn-block" onclick="return confirm('Are you sure you want to delete this station?');">Delete</button>
                                </form>
                            </td>
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