var projectMarkers = [];
var geophysicMarkers = [];
var map;

function initGeophyMap() {
    // Initialize the map without a specific center and zoom level
    var myOptions = {
        zoom: 7,
        panControl: false,
        streetViewControl: false,
        mapTypeControl: true,
        mapTypeControlOptions: { style: google.maps.MapTypeControlStyle.DROPDOWN_MENU },
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoomControl: true,
        zoomControlOptions: { style: google.maps.ZoomControlStyle.SMALL }
    };
    map = new google.maps.Map(document.getElementById("geophyMap"), myOptions);

    // Fetch and display both projects and geophysical data on the map
    fetchProjAndSetMarkers();
    const geophysical_id = document.getElementById("geophysicalId").getAttribute("data-geophysical-id");
    fetchGeophyAndSetMarkers(geophysical_id);
}

function fetchProjAndSetMarkers() {
    const project_id = document.getElementById("projectId").getAttribute("data-project-id");

    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {
            // Find the specific project by project_id
            const targetProject = data.find(project => project.id.toString() === project_id);

            if (targetProject) {
                // Set map center based on the specific project coordinates
                const centerCoordinates = {
                    lat: parseFloat(targetProject.proj_latitude),
                    lng: parseFloat(targetProject.proj_longitude)
                };
                map.setCenter(centerCoordinates);
                map.setZoom(15); // Adjust zoom level as desired

                // Update markers for all projects (optional)
                updateProjMapMarkers(data);
            } else {
                console.error("Project not found");
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function fetchGeophyAndSetMarkers(geophysical_id) {
    fetch(`/api/geophysic_seismic/${geophysical_id}`)
        .then(response => response.json())
        .then(data => {
            updateGeophyMapMarkers(data);
            drawGeophyLine(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateProjMapMarkers(projects) {
    const project_id = document.getElementById("projectId").getAttribute("data-project-id");

    // Remove existing project markers from the map
    projectMarkers.forEach(marker => marker.setMap(null));
    projectMarkers = [];

    projects.forEach(project => {
        // Only add the marker if the project ID does not match the excluded project_id
        if (project.id.toString() !== project_id) {
            var marker = new google.maps.Marker({
                position: { lat: parseFloat(project.proj_latitude), lng: parseFloat(project.proj_longitude) },
                map: map,
                title: project.projects_name,
                icon: {
                    url: '/static/img/proj_location.svg',
                    scaledSize: new google.maps.Size(30, 30)
                }
            });
            attachProjInfoWindow(marker, project);
            projectMarkers.push(marker);
        }
    });
}

function fitMapToProjectBounds(projects) {
    const bounds = new google.maps.LatLngBounds();
    projects.forEach(project => {
        const position = new google.maps.LatLng(parseFloat(project.proj_latitude), parseFloat(project.proj_longitude));
        bounds.extend(position);
    });

    // Adjust the map to fit the bounds of all project markers
    map.fitBounds(bounds);
}

function updateGeophyMapMarkers(geophysics) {
    // Remove existing geophysical markers from the map
    geophysicMarkers.forEach(marker => marker.setMap(null));
    geophysicMarkers = [];

    geophysics.forEach(geophysic => {
        // Create marker for the starting point
        const startMarker = new google.maps.Marker({
            position: { lat: parseFloat(geophysic.first_latitude), lng: parseFloat(geophysic.first_longitude) },
            map: map,
            title: geophysic.vs30 ? `Start - VS30: ${geophysic.vs30}` : 'Start - ----',
            icon: {
                url: '/static/img/geophy_loc.svg',
                scaledSize: new google.maps.Size(30, 30)
            }
        });
        attachGeophyInfoWindow(startMarker, geophysic, "Start");
        geophysicMarkers.push(startMarker);

        // Create marker for the ending point
        const endMarker = new google.maps.Marker({
            position: { lat: parseFloat(geophysic.second_latitude), lng: parseFloat(geophysic.second_longitude) },
            map: map,
            title: geophysic.vs30 ? `End - VS30: ${geophysic.vs30}` : 'End - ----',
            icon: {
                url: '/static/img/geophy_loc.svg',
                scaledSize: new google.maps.Size(30, 30)
            }
        });
        attachGeophyInfoWindow(endMarker, geophysic, "End");
        geophysicMarkers.push(endMarker);
    });
    
}

// Draw a line between two geophysical points
function drawGeophyLine(data) {
    data.forEach(geophysic => {
        const lineCoordinates = [
            { lat: parseFloat(geophysic.first_latitude), lng: parseFloat(geophysic.first_longitude) },
            { lat: parseFloat(geophysic.second_latitude), lng: parseFloat(geophysic.second_longitude) }
        ];
        
        const line = new google.maps.Polyline({
            path: lineCoordinates,
            geodesic: true,
            strokeColor: "#FF0000", // Red color for visibility
            strokeOpacity: 1.0,
            strokeWeight: 2
        });
        
        line.setMap(map);
    });
}

function attachProjInfoWindow(marker, project) {
    var infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="text-center">
                <strong>პროექტის სახელი: ${project.projects_name}</strong><br>
                დაწყების დღე: ${project.start_time}<br>
                დასრულების დღე: ${project.end_time}<br>
                დამკვეთი: ${project.contractor || '----'}<br>
                განედი: ${project.proj_latitude}<br>
                გრძედი: ${project.proj_longitude}<br>
                VS30: ${project.geophysical.length > 0 ? project.geophysical[0].vs30 : '----'}<br>
                PGA 10%: ----<br>
                <a style="display:block; margin-top:20px" href="/view_project/${project.id}">დეტალურად</a>
            </div>`
    });
    marker.addListener('click', function () {
        infoWindow.open(map, marker);
    });
}

function attachGeophyInfoWindow(marker, geophysic, pointType) {
    var infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="text-center">
                <strong>${pointType} Point</strong><br>
                VS30: ${geophysic.vs30 ? geophysic.vs30 : '----'}<br>
                განედი (y): ${pointType === "Start" ? geophysic.first_latitude : geophysic.second_latitude}<br>
                გრძედი (x): ${pointType === "Start" ? geophysic.first_longitude : geophysic.second_longitude}<br>
                <a style="display:block; margin-top:20px" href="/view_geophysical/${geophysic.id}">დეტალურად</a>
            </div>`
    });
    marker.addListener('click', function () {
        infoWindow.open(map, marker);
    });
}

// Initialize the map when the page loads
document.addEventListener("DOMContentLoaded", function () {
    initGeophyMap();
});