/*
 * This is part of Fahrwerk's online ordering form. Please do not abuse the
 * Mapbox access token.
 */

MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoiam5ucyIsImEiOiJjaW1kdjlpMXYwMDM2dnVtM2FhbXk5bGg2In0.UVYyozEY2m-LlMqLp0EhCw";
L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;
var map = L.mapbox.map('map', 'mapbox.streets', {attributionControl: {compact: true}}).
	setView([52.52, 13.37], 13);