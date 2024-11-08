var projectMarkers = [];
var geophysicMarkers = [];
var map;

function initGeophyMap() {
    var latlng = new google.maps.LatLng(42.264, 43.322);
    var myOptions = {
        zoom: 7,
        center: latlng,
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
    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {
            updateProjMapMarkers(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function fetchGeophyAndSetMarkers(geophysical_id) {
    fetch(`/api/geophysic_seismic/${geophysical_id}`)
        .then(response => response.json())
        .then(data => {
            updateGeophyMapMarkers(data);
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

function updateGeophyMapMarkers(geophysics) {
    // Remove existing geophysical markers from the map
    geophysicMarkers.forEach(marker => marker.setMap(null));
    geophysicMarkers = [];

    geophysics.forEach(geophysic => {
        var marker = new google.maps.Marker({
            position: { lat: parseFloat(geophysic.latitude), lng: parseFloat(geophysic.longitude) },
            map: map,
            title: geophysic.vs30 ? geophysic.vs30.toString() : '----',
            icon: {
                url: '/static/img/geophy_loc.svg',
                scaledSize: new google.maps.Size(30, 30)
            }
        });
        attachGeophyInfoWindow(marker, geophysic);
        geophysicMarkers.push(marker);
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

function attachGeophyInfoWindow(marker, geophysic) {
    var infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="text-center">
                VS30: ${geophysic.vs30 ? geophysic.vs30 : '----'}<br>
                PGA 10%: ----<br>
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