var stations = [];

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
    var map = new google.maps.Map(document.getElementById("map"), myOptions);
    fetchAndSetMarkers(map);
}

function fetchAndSetMarkers(map) {
    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {
            projects = data;
            setMarkers(map);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function setMarkers(map) {
    for (var i = 0; i < projects.length; i++) {
        var project = projects[i];
        var marker = new google.maps.Marker({
            position: {lat: parseFloat(project.proj_latitude), lng: parseFloat(project.proj_longitude)},
            map: map,
            title: project.projects_name,
            icon: {
                url: 'https://cdn-icons-png.flaticon.com/128/13379/13379300.png',
                scaledSize: new google.maps.Size(30, 30)
            }
        });
        attachInfoWindow(marker, project);
    }
}

function attachInfoWindow(marker, project) {
    var infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="text-center">
                <strong>პროექტის სახელი: ${project.projects_name}</strong><br>
                ხელშეკრულების ნომერი: ${project.contract_number}<br>
                დაწყების დღე: ${project.start_time}<br>
                დასრულების დღე: ${project.end_time}<br>
                დამკვეთი: ${project.contractor}<br>
                განედი: ${project.proj_latitude}<br>
                გრძედი: ${project.proj_longitude}<br>
                VS30: 600<br>
                PGA 10%: 0.25<br>
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