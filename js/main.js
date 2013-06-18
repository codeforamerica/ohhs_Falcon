$(function(){
  

  var map = L.map('map').setView([37.7749295, -122.4494155], 12);
  var mapquestUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
  subDomains = ['otile1','otile2','otile3','otile4'],
  mapquestAttrib = 'Data by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.'
  var mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 18, attribution: mapquestAttrib, subdomains: '1234'});

  map.addLayer(mapquest);


});
