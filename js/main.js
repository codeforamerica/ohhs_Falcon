var map;
$(function(){
  
  map = L.map('map').setView([37.767745, -122.441475], 12);
  var mapquestUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
  subDomains = ['otile1','otile2','otile3','otile4'],
  mapquestAttrib = 'Data by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.'
  var mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 19, attribution: mapquestAttrib, subdomains: '1234'});

  map.addLayer(mapquest);
  
  function onLocationFound(location)
  {
    var ne = location.bounds._northEast,
        sw = location.bounds._southWest;
    
    if(location.accuracy > 500)
    {
        // accuracy of location in meters > 500m, which means we really
        // don't know where someone is. Do something here to flag that.
        return alert("couldn't locate you with sufficient accuracy");
    }
    
    map.setView({lat: ne.lat/2 + sw.lat/2, lng: ne.lng/2 + sw.lng/2}, 18);
  }
  
  map.on('locationfound', onLocationFound);
  map.locate({setView: false, maxZoom: 19});

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

  var geojsonURL = 'http://data.codeforamerica.org/OHHS/SF/1.2/tiles/{z}/{x}/{y}.json';
  var geojsonTileLayer = new L.TileLayer.GeoJSON(geojsonURL, {
    unique: function (feature) { return feature.properties.id; },
    maxZoom:20
  }, {
    style: style,
    onEachFeature: function (feature, layer) {

      layer.on("click", function(){
        
        map.panTo(layer._latlng)

        var infoString = '<div>';
        for (var k in feature.properties) {
          var v = feature.properties[k];
          infoString += k + ': ' + v + '<br />';
        }
        infoString += '</div>';
        $("div#housinginfo").html(infoString);
        
        console.log(feature, layer)

      });
    }
  });
  map.addLayer(geojsonTileLayer);


  $("#addressentry").on("submit", function(e){
    e.preventDefault();

    var url = "http://open.mapquestapi.com/geocoding/v1/address";

    var data = {outFormat:"json",
                inFormat:"kvp",
                key:"Fmjtd|luua2q6and,aa=o5-hzb59",
                boundingBox:"37.816,-122.536,37.693,-122.340",
                location:$("#address").val() + ', San Francisco'};

    $.ajax(url, {data:data, dataType:"jsonp", success:function(data){
      console.log(data)
      //TODO: check for errors
      map.panTo([data.results[0].locations[0].latLng.lat, data.results[0].locations[0].latLng.lng]);

    }});

  });



});
