var map;

var __defaults = {
    city_name: 'San Francisco',
    data_url: 'http://data.codeforamerica.org/OHHS/SF/1.2',
    bounds: [37.816, -122.536, 37.693, -122.340],
    center: [37.767745, -122.441475],
    mapquest_key: "Fmjtd|luua2q6and,aa=o5-hzb59"
    };

//
// map.setView() with a check for SF bounds.
//
function boundedSetView(center)
{
    var bounds = __defaults.bounds;
    
    if(center.lat > bounds[0] || center.lng < bounds[1] || center.lat < bounds[2] || center.lng > bounds[3])
    {
        // found location is outside of default city, so we will not set the view.
        return alert("You were about to look outside of "+__defaults.city_name+" - try searching for an address inside the city?");
    }
    
    map.setView(center, 18);
}

//
// Callback function for browser geolocation.
// http://leafletjs.com/reference.html#map-locate
//
function onLocationFound(location)
{
    var ne = location.bounds._northEast,
        sw = location.bounds._southWest,
        center = new L.LatLng(ne.lat/2 + sw.lat/2, ne.lng/2 + sw.lng/2);
    
    if(location.accuracy > 500)
    {
        // accuracy of location in meters > 500m, which means we really
        // don't know where someone is. Do something here to flag that.
        return alert("couldn't locate you with sufficient accuracy");
    }
    
    return boundedSetView(center);
}

//
// Callback function for geocode results from Mapquest Open.
// http://open.mapquestapi.com/geocoding/
//
function onAddressFound(response)
{
    var center = response.results[0].locations[0].latLng;
    return boundedSetView(center);
}

//
// Set up map, but don't set the view to anything.
//
function setupMap(element)
{
    var map = L.map('map'),
        mapquestUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
        subDomains = ['otile1','otile2','otile3','otile4'],
        mapquestAttrib = 'Data by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.',
        mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 19, attribution: mapquestAttrib, subdomains: '1234'});
    
    map.addLayer(mapquest);
    
    return map;
}

//
// Callback function for a loaded building.
//
function onBuildingLoaded(building)
{
    boundedSetView(new L.LatLng(building.latitude, building.longitude));
}

var falcon = {

  showBuildingDetails:function(building){
    console.log("details", building);
    var address = "";

    if(building.from_street_num === building.to_street_num)
      address += building.from_street_num;
    else
      address += building.from_street_num + "-"+ building.to_street_num

    address += " "+building.street +" "+ building.st_type+". "+ building.city+", "+ building.state + " "+  building.postal_code;

    
    var totalViolations = 0,
        recentInspectionDate = null;

    if(!building.inspections)
      building.inspections = [];

    for(i in building.inspections){
      var insp = building.inspections[i];
      if(!insp.violations)
        insp.violations =[];
      console.log(insp);
      totalViolations += insp.violations.length;
      insp.groupedViolations = {};
      for(v in insp.violations){
        var vio = insp.violations[v];
        if(vio.category+":"+vio.type in insp.groupedViolations)
          insp.groupedViolations[vio.category+":"+vio.type].count +=1;
        else
          insp.groupedViolations[vio.category+":"+vio.type] = {count:1, type:vio.type, category:vio.category, date_closed:vio.date_closed};
      }
    }
    

    var detailHTML = "<div class='address'>"+address+"</div>";
    detailHTML += "<div class='ownername'>"+building.owner_name+"</div>";
    detailHTML += "<div class='propertyid'>Property Id: "+building.id+"</div>";
    detailHTML += "<div class='inspections'> This building has been inspected "+building.inspections.length+" times, most recently June 2012</div>";
    detailHTML += "<div class='violations'>There "+ (totalViolations > 1 ? "has" : "have")+" been "+totalViolations+" violation"+(totalViolations > 1 ? "s" : "")+": <ul>"
    for(i in building.inspections){
      var insp = building.inspections[i];
      if(insp.violations.length === 0)
        continue;
      var violationString = "";
      for(v in insp.groupedViolations){
        var vio = insp.groupedViolations[v];
        violationString += " "+ vio.count+" "+vio.category + " (" + vio.type + ") violation"+(vio.count > 1 ? "s were" : " was")+" found, ";
        if(vio.date_closed)
          violationString += " and "+(vio.count > 1 ? "were": "was")+" closed "+ vio.date_closed;
        else
          violationString+= " and "+(vio.count > 1 ? "were": "was")+" never resolved."
      }

      detailHTML += "<li>";

      if(insp.type === "Complaint")
        detailHTML += "During an inspection due to a complaint on ";
      else if(insp.type === "Routine")
        detailHTML += "During a routine inspection on";
      else if(insp.type === "Followup")
        detailHTML += "<li> During a followup inspection on ";
      detailHTML += insp.date+ " "+ violationString+"</li>"
      
    }

    detailHTML += "</ul></div>"
    
    detailHTML += "<div class='details'>The building is a "+building.sqft+" sqft "+ building.type+" with "+
      building.dwelling_units+" units built in "+ building.built_year+", currently assessed at $"+building.value+".</div>"; 
    
    detailHTML += "<div class='ownercontact'>Contact the owner at "+building.owner_mailing_address+"</div>";
    detailHTML += "<div class='contactinfo'>SFDPH Contact Info</div>"
    
    $("div#housinginfo").html(detailHTML);

  }

};


$(function(){

  map = setupMap('map');
  
  if(location.hash.match(/^#\w+$/)) {
    //
    // Found what looks like a building ID in the URL, so use it.
    //
    var building_id = location.hash.replace(/^#(\w+)$/, '$1'),
        building_url = __defaults.data_url+'/buildings/'+building_id+'.json';

    $.ajax(building_url, {success: onBuildingLoaded})

  } else {
    //
    // Otherwise, just pick out the center of the city and then try geolocating.
    //
    map.setView(__defaults.center, 12);
    map.on('locationfound', onLocationFound);
    map.locate({setView: false, maxZoom: 19});
  }

  var geojsonURL = __defaults.data_url+'/tiles/{z}/{x}/{y}.json';
  var buildingIcon = L.icon({iconUrl: 'img/falcon_map_marker@1x.png',
                             iconRetinaUrl: 'img/falcon_map_marker@2x.png',
                             iconSize: [31, 41],
                             iconAnchor: [14, 41]});
  var buildingIconActive = L.icon({iconUrl: 'img/falcon_map_marker_active2@1x.png',
                             iconRetinaUrl: 'img/falcon_map_marker_active2@2x.png',
                             iconSize: [31, 41],
                             iconAnchor: [14, 41]});

  var activeMarker = null;

  var geojsonTileLayer = new L.TileLayer.GeoJSON(geojsonURL, {
    unique: function (feature) { return feature.properties.id; },
    maxZoom:20
  }, {
    pointToLayer: function(feature, latlng){

      return L.marker(latlng, {icon:buildingIcon});
    },
    onEachFeature: function (feature, layer) {

      if(activeMarker == layer)
        layer.setIcon(buildingIconActive);

      layer.on("click", function(){
        map.panTo(layer._latlng);
        falcon.showBuildingDetails(feature.properties);


        if(activeMarker)
          activeMarker.setIcon(buildingIcon);
        this.setIcon(buildingIconActive);
        activeMarker = this;
      });
    }
  });
  map.addLayer(geojsonTileLayer);


  $("#addressentry").on("submit", function(e){
    e.preventDefault();

    var url = "http://open.mapquestapi.com/geocoding/v1/address";

    var data = {outFormat:"json",
                inFormat:"kvp",
                key:__defaults.mapquest_key,
                boundingBox:"37.816,-122.536,37.693,-122.340",
                location:$("#address").val() + ', ' + __defaults.city_name};
    
    $.ajax(url, {data: data, dataType: 'jsonp', success: onAddressFound});

  });


});
