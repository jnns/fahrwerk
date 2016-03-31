/*
 * This is part of Fahrwerk's online ordering form. Please do not abuse the
 * Mapbox access token.
 */

MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoiam5ucyIsImEiOiJjaW1kdjlpMXYwMDM2dnVtM2FhbXk5bGg2In0.UVYyozEY2m-LlMqLp0EhCw";

L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

var markers = {};
var route = {};
var map = L.mapbox.map('map', 'mapbox.streets', {attributionControl: {compact: true}}).
	setView([52.52, 13.37], 13);

function setMarker(query, location) {
	$.getJSON("http://photon.komoot.de/api/", {
		q: query,
		lat: 52.52,
		lon: 13.37
		},
		function(response) {
			markers[location] = t = response.features[0];

			// Reorder coordinates to Lat,Lng because Photon uses a different
			// order than Leaflet/Mapbox.
			var coords = [
				t.geometry.coordinates[1],
				t.geometry.coordinates[0]
			];

			if ("marker" in markers[location]) {
				t.marker.setLatLng(coords);
			} else {
				t.marker = L.marker(coords).addTo(map);
			}

			map.setView(t.marker.getLatLng());
			markerSet();
		}
	);
}

function markerSet() {
	if ("origin" in markers && "destination" in markers) {
		// AARGH what a hack. I should use the javascript-sdk but I don't want
		// to go through bundling and all that shit. What a mess.
		// Only because geometries are reversed in OSM.
		var coords = markers.origin.geometry.coordinates[0] + "," +
					 markers.origin.geometry.coordinates[1] + ";" +
					 markers.destination.geometry.coordinates[0] + "," +
					 markers.destination.geometry.coordinates[1];
		var API_URL = "https://api.mapbox.com/v4/directions/mapbox.driving/" + coords +".json";
		$.getJSON(API_URL, {access_token: MAPBOX_ACCESS_TOKEN}, function (response) {
			route = response;
			routeCalculated();
		});
	}
}

function routeCalculated() {
	map.featureLayer.setGeoJSON(route.routes[0].geometry);
	map.fitBounds(map.featureLayer.getBounds());
}

$(function() {
	$(".quickstart__from").change(function () { setMarker(this.value, "origin")});
	$(".quickstart__to").change(function () { setMarker(this.value, "destination")});
});