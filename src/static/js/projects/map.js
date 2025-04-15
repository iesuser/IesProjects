let graphicsLayer;

require([
  "esri/Map",
  "esri/views/MapView",
  "esri/Graphic",
  "esri/layers/GraphicsLayer"
], (Map, MapView, Graphic, GraphicsLayer) => {

  const map = new Map({
    basemap: "hybrid"
  });

  const view = new MapView({
    container: "map",
    map: map,
    zoom: 7,
    center: [42.0, 41.8]
  });

  graphicsLayer = new GraphicsLayer();
  map.add(graphicsLayer);

  // Make the update function globally available
  window.updateArcgisMarkers = function (projects) {
    graphicsLayer.removeAll(); // Clear existing markers
    projects.forEach(project => {
      const pointGraphic = new Graphic({
        geometry: {
          type: "point",
          latitude: project.proj_latitude,
          longitude: project.proj_longitude
        },
        symbol: {
          type: "picture-marker",
          url: "static/img/proj_location.svg", // Change to your image URL
          width: "35px",
          height: "35px"
        },
        attributes: {
          id: project.id,  // ✅ Explicitly set it first
          ...project,
          vs30: project.geophysical?.[0]?.vs30 || "N/A"
        },
        popupTemplate: {
          title: "{projects_name}",
          content: function (graphic) {
            const attr = graphic.graphic.attributes;
            const id = attr.id || attr._id || "unknown"; // fallback in case of data issues
            return `
              <b>დაწყების დღე:</b> ${attr.start_time}<br>
              <b>დასრულების დღე:</b> ${attr.end_time}<br>
              <b>დამკვეთი:</b> ${attr.contractor}<br>
              <b>განედი:</b> ${attr.proj_latitude}<br>
              <b>გრძედი:</b> ${attr.proj_longitude}<br>
              <b>Vs30:</b> ${attr.vs30}<br>
              <a href="${window.location.href}/view_project/${attr.id}">დეტალურად</a>
            `;
          }
        }
      });

      graphicsLayer.add(pointGraphic);
    });
  };
});
