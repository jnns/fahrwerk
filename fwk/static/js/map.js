/*
 * This is part of Fahrwerk's online ordering form. Please do not abuse the
 * Mapbox access token.
 */

MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoiam5ucyIsImEiOiJjaW1kdjlpMXYwMDM2dnVtM2FhbXk5bGg2In0.UVYyozEY2m-LlMqLp0EhCw";

L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

var markers = {origin: {}, destination: {}};
var route = {};
var locations = {};
var map = L.mapbox.map('map', 'mapbox.streets', {attributionControl: {compact: true}}).
	setView([52.52, 13.37], 13);

function markerSet(location) {

	// fill pickup address form field
	if (location == "origin") {
		pickup = markers.origin.properties;
	} else if (location == "destination") {
		dropoff = markers.destination.properties;
	}

	if (quickstartBox.bothAddressesSet()) {
		// AARGH what a hack. I should use the javascript-sdk but I don't want
		// to go through bundling and all that shit. What a mess.
		// Only because geometries are reversed in OSM.
		var coords = markers.origin.marker.getLatLng()[0] + "," +
					 markers.origin.marker.getLatLng[1] + ";" +
					 markers.destination.marker.getLatLng[0] + "," +
					 markers.destination.marker.getLatLng[1];
		var API_URL = "https://api.mapbox.com/v4/directions/mapbox.driving/" + coords +".json";
		$.getJSON(API_URL, {access_token: MAPBOX_ACCESS_TOKEN}, function (response) {
			route = response;
			routeCalculated();
		});
	}
}

/*
 * Not important anymore because state changes are handled by the react
 * component now.

$(function() {
	$(".quickstart__from").change(function () { geocodeAndSetMarker(this.value, "origin")});
	$(".quickstart__to").change(function () { geocodeAndSetMarker(this.value, "destination")});
});
*/