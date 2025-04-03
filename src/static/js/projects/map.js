let view, graphicsLayer;

require([
  "esri/Map",
  "esri/views/MapView",
  "esri/Graphic",
  "esri/layers/GraphicsLayer",
  "esri/widgets/Popup"
], function(Map, MapView, Graphic, GraphicsLayer) {

  // Initialize the map
  const map = new Map({ basemap: "hybrid" });

  // Create the view
  view = new MapView({
    container: "viewDiv",
    map: map,
    center: [43.322, 42.264], // Longitude, Latitude
    zoom: 7
  });

  // Layer for markers
  graphicsLayer = new GraphicsLayer();
  map.add(graphicsLayer);

  // Initialize with an empty array
  let markers = [];

  // Sample projects data (replace with actual data)
  const projects = [
    {
      id: 1,
      projects_name: "პროექტი 1",
      proj_latitude: 42.5,
      proj_longitude: 43.5,
      start_time: "2024-03-01",
      end_time: "2024-06-01",
      contractor: "კომპანია A",
      geophysical: [{ vs30: 300 }]
    },
    {
      id: 2,
      projects_name: "პროექტი 2",
      proj_latitude: 42.8,
      proj_longitude: 43.2,
      start_time: "2024-01-15",
      end_time: "2024-04-20",
      contractor: null,
      geophysical: []
    }
  ];

  // Load markers on map
  updateMapMarkers(projects);

  // Function to update markers
  function updateMapMarkers(projects) {
    graphicsLayer.removeAll(); // Clear previous markers

    projects.forEach(project => {
      const point = {
        type: "point",
        longitude: parseFloat(project.proj_longitude),
        latitude: parseFloat(project.proj_latitude)
      };

      const markerSymbol = {
        type: "picture-marker",
        url: "/static/img/proj_location.svg", // Custom marker icon
        width: "30px",
        height: "30px"
      };

      const pointGraphic = new Graphic({
        geometry: point,
        symbol: markerSymbol,
        attributes: project,
        popupTemplate: {
          title: `📍 პროექტი: {projects_name}`,
          content: `
            <strong>დაწყების დღე:</strong> {start_time} <br>
            <strong>დასრულების დღე:</strong> {end_time} <br>
            <strong>დამკვეთი:</strong> {contractor} <br>
            <strong>განედი:</strong> {proj_latitude} <br>
            <strong>გრძედი:</strong> {proj_longitude} <br>
            <strong>VS30:</strong> ${project.geophysical.length > 0 ? project.geophysical[0].vs30 : '----'} <br>
            <a href="/view_project/${project.id}" target="_blank">➡ დეტალურად</a>
          `
        }
      });

      graphicsLayer.add(pointGraphic);
      markers.push(pointGraphic);
    });
  }
});