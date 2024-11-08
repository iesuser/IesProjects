var markers = [];
var map;

function initMap() {
    var latlng = new google.maps.LatLng(42.264, 43.322);
    var myOptions = {
        zoom: 7,
        center: latlng,
        panControl: false,
        streetViewControl: false,
        mapTypeControl: true,
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoomControl: true,
        zoomControlOptions: {style: google.maps.ZoomControlStyle.SMALL}
    };
    map = new google.maps.Map(document.getElementById("map"), myOptions);
}

function updateMapMarkers(projects) {
    // Remove existing markers from the map
    markers.forEach(marker => marker.setMap(null));
    markers = []; // Clear the markers array

    projects.forEach(project => {
        var marker = new google.maps.Marker({
            position: {lat: parseFloat(project.proj_latitude), lng: parseFloat(project.proj_longitude)},
            map: map,
            title: project.projects_name,
            icon: {
                url: '/static/img/proj_location.svg',
                scaledSize: new google.maps.Size(30, 30)
            }
        });
        attachInfoWindow(marker, project);
        markers.push(marker); // Add marker to the array
    });
}

function attachInfoWindow(marker, project) {
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
    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });
}

// Initialize the map when the page loads
document.addEventListener("DOMContentLoaded", function() {
    initMap();
});