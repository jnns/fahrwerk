/*
 * Quickstart is the component which renders the initial two input boxes for
 * pickup and delivery that enables users to quickly get a quotation on the
 * delivery rates.
 *
 * It delegates setting markers and route on the interactive map and handles
 * JSON requests to the backend.
 */

// minimum required length of input value for querying the backend
var INPUT_MIN_LENGTH = 5;
var GEOCODE_URL = "http://photon.komoot.de/api/";

var QuickstartBox = React.createClass({
    componentDidMount: function () {
        // In case of Django re-rendering the form, kick off route drawing and
        // price calculation
        if (this.bothAddressesSet()) {
           this.geocode(this.state.pickup, "pickup");
           this.geocode(this.state.dropoff, "dropoff");
        }
        // Throttle API calls by using underscore.js's debounce function.
        this.geocode = _.debounce(this.geocode, 750);
    },
    getInitialState: function() {
        // If Django re-renders the form, use the supplied values to set the
        // initial state
        var pickup = ($("#id_from_street").val() +" "+ $("#id_from_zipcode").val()).trim();
        var dropoff = ($("#id_to_street").val() +" "+ $("#id_to_zipcode").val()).trim();

        return {
            pickup: pickup,
            dropoff: dropoff,
            geocoded: {
                pickup: {},
                dropoff: {}
            },
            markers: {},  //  L.marker information
            price: '',
            packages_s: 0,
            packages_m: 0,
            packages_l: 0
        }
    },
    geocode: function (input, pu_or_do) {
        // set coordinate bias to Berlin's center
        var data = {q: input, lat: 52.52, lon: 13.37};
        $.getJSON(GEOCODE_URL, data, function (response) {
            this.setMarker(response, pu_or_do);
        }.bind(this));
    },
    setMarker: function (data, pu_or_do) {
        this.state.geocoded[pu_or_do] = data.features[0];
        var obj = this.state.geocoded[pu_or_do]; // current target

        // set icon
        var icon;
        if (pu_or_do == 'pickup') {
            icon = '1';
        } else {
            icon = '2';
        }

        // try to set tooltip
        var p = obj.properties;

        var coords = [obj.geometry.coordinates[1], obj.geometry.coordinates[0]];
        if (this.state.markers[pu_or_do]) {
            // delete existing marker
            map.removeLayer(this.state.markers[pu_or_do]);
        }

        // add new marker to map
        var options = {
            icon: L.mapbox.marker.icon({
                'marker-symbol': icon,
                'marker-size': 'large',
                'marker-color': '#84329B'
            }),
        };
        var description;
        try {
            description = "<b>"+p.name+"</b><br> "+p.street + " " + p.housenumber + " " + p.postcode + " " + p.city
        } catch (e) {
            description = "";
        }
        this.state.markers[pu_or_do] = L.marker(coords, options).bindPopup(description).addTo(map);

        map.panTo(this.state.markers[pu_or_do].getLatLng());
        this.markerHasBeenSet(data, pu_or_do);
    },
    handlePickupChange: function(e) {
        var input = e.target.value;
        this.setState({ pickup: input });
        if (input.length >= INPUT_MIN_LENGTH) {
            this.geocode(input, "pickup");
        }
    },
    handleDropoffChange: function(e) {
        var input = e.target.value;
        this.setState({ dropoff: input });
        if (input.length >= INPUT_MIN_LENGTH) {
            this.geocode(input, "dropoff");
        }
    },
    // these functions are only needed because I don't really know how to make
    // use of React and Django form validation at the same time. It'd be much
    // cleaner if this could also be a React component on itw own.
    handlePackageSChange: function() {
        this.setState({packages_s: $("#id_packages_s").val() });
        this.loadPrice();
    },
    handlePackageMChange: function() {
        this.setState({packages_m: $("#id_packages_m").val() });
        this.loadPrice();
    },
    handlePackageLChange: function() {
        this.setState({packages_l: $("#id_packages_l").val() });
        this.loadPrice();
    },
    markerHasBeenSet: function (data, pu_or_do) {

        // update appropriate form field with address
        var p = this.state.geocoded[pu_or_do].properties;
        var name = p.name || "";
        var street = (p.street || "") + " " + (p.housenumber || "").trim();
        var postcode = p.postcode || "";

        if (pu_or_do == "pickup") {
            $("#id_from_company").val(name);
            $("#id_from_street").val(street);
            $("#id_from_zipcode").val(postcode);
        } else {
            $("#id_to_company").val(name);
            $("#id_to_street").val(street);
            $("#id_to_zipcode").val(postcode);
        }

        // calculate route if all necessary informations are supplied
        if (this.bothMarkersSet()) {
            this.drawRoute();
        } else { console.log("Would query API for price if form was valid (i.e. pickup and (!) dropoff present).") }
    },
    loadPrice: function() {
        if (this.state.route) {
            $.ajax({
                url: this.props.url,
                dataType: 'json',
                data: {
                    distance: this.state.route.distance / 1000,
                    s: this.state.packages_s,
                    m: this.state.packages_m,
                    l: this.state.packages_l
                },
                cache: false,
                success: function(data) {
                    this.setState({price: data});
            }.bind(this),
                error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                }.bind(this)
            });
        } else { console.log("No route available, yet. Therefore no price can be calculated."); }
    },
    drawRoute: function() {
        // Alright, I know this is messy – but it's straightfoward. Different
        // APIs return longitute and latitude in different order and as much
        // as I'd like to just use Mapbox-sdk-js, it's just not feasible. This
        // is the case because it would introduce a lot of dependencies I'm
        // not familiar with (e.g. browserify).
        var pu = this.state.markers["pickup"].getLatLng();
        var droff = this.state.markers["dropoff"].getLatLng();
        var coords = pu.lng + "," + pu.lat + ";" + droff.lng + ","+ droff.lat;

        var API_URL = "https://api.mapbox.com/v4/directions/mapbox.driving/" + coords +".json";
        $.getJSON(API_URL, {access_token: MAPBOX_ACCESS_TOKEN}, function (response) {
            this.state.directions_result = response;
            try {
                var route = this.state.route = response.routes[0];
                // fixup
                route["type"] = "Feature";
                route["properties"] = {
                    "stroke": "#84329B",
                    "stroke-width": 8,
                    "stroke-opacity": 0.8,
                    "lineCap": "round",
                    "lineJoin": "round",
                    "clickable": false
                };
                map.featureLayer.setGeoJSON(route);

                /*map.addSoure("route", {

                });
                */
                map.fitBounds(map.featureLayer.getBounds());
                this.loadPrice();
            } catch (e) {
                console.log(response.error);
            }
        }.bind(this));
    },
    bothAddressesSet: function () {
        if (this.state.pickup && this.state.dropoff) {
            return true;
        }
        return false;
    },
    bothMarkersSet: function () {
        if (this.state.markers["pickup"] && this.state.markers["dropoff"]) {
            return true;
        }
        return false;
    },
    render: function () {
        var price = (this.state.price || 0).toLocaleString("de", {style: "currency", currency: "EUR", minimumFractionDigits: 2})
        return (
            <div className="quickstart__wrapper">
                <form className="quickstart">
                    <input type="text" className="quickstart__from" placeholder="Abholadresse" value={this.state.pickup} onChange={this.handlePickupChange} />
                    <span className="quickstart__arrow">🡆</span>
                    <input type="text" className="quickstart__to" placeholder="Zustelladresse" value={this.state.dropoff} onChange={this.handleDropoffChange} />
                </form>
                <div className="quickstart__price">Preis: {price} <a href="#*">*</a></div>
            </div>
        );
    }
});

React.createClass({

});

// render QuickstartBox and make it available to map.js under `quickstartBox`.
window.quickstartBox = ReactDOM.render(
    <QuickstartBox url="/api/v1/price/" />,
    document.getElementById('quickstart'));