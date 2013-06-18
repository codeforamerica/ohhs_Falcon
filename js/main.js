$(function(){
  

  var map = L.map('map').setView([37.7749295, -122.4494155], 17);
  var mapquestUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
  subDomains = ['otile1','otile2','otile3','otile4'],
  mapquestAttrib = 'Data by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.'
  var mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 20, attribution: mapquestAttrib, subdomains: '1234'});

  map.addLayer(mapquest);

//https://raw.github.com/smartchicago/chicago-atlas/master/db/import/zipcodes.geojson

  var style = {
    "clickable": true,
    "color": "#00D",
    "fillColor": "#00D",
    "weight": 1.0,
    "opacity": 0.3,
    "fillOpacity": 0.2
  };
  var hoverStyle = {
    "fillOpacity": 0.5
  };

  var geojsonURL = 'http://data.codeforamerica.org.global.prod.fastly.net/OHHS/SF/1.2/tiles/{z}/{x}/{y}.json';
  var geojsonTileLayer = new L.TileLayer.GeoJSON(geojsonURL, {
    unique: function (feature) { return feature.properties.id; },
  }, {
    style: style,
    onEachFeature: function (feature, layer) {
      if (feature.properties) {
        var popupString = '<div class="popup">';
        for (var k in feature.properties) {
          var v = feature.properties[k];
          popupString += k + ': ' + v + '<br />';
        }
        popupString += '</div>';
        layer.bindPopup(popupString);
      }
    }
  });
  map.addLayer(geojsonTileLayer);


});
