var map;
$(function(){
  
  map = L.map('map').setView([37.7749295, -122.4494155], 17);
  var mapquestUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
  subDomains = ['otile1','otile2','otile3','otile4'],
  mapquestAttrib = 'Data by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.'
  var mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 19, attribution: mapquestAttrib, subdomains: '1234'});

  map.addLayer(mapquest);
  map.locate({setView:true, maxZoom:19})

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
                boundingBox:"37.8059864,-122.5463104,37.6930576,-122.3396301",
                location:$("#address").val()};

    $.ajax(url, {data:data, dataType:"jsonp", success:function(data){
      console.log(data)
      //TODO: check for errors
      map.panTo([data.results[0].locations[0].displayLatLng.lat, data.results[0].locations[0].displayLatLng.lng]);

    }});

  });



});
