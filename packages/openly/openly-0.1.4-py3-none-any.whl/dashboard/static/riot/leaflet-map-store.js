/**
 * Creates a RiotControl store which provides wrappers for a lot of
 * the common use cases we have for location mapping
 * @param store_opts
 * @constructor
 */
function LeafletMapStore(store_opts) {
    var store = this;
    riot.observable(store);
    store_opts = _.defaults({}, store_opts, {
        map_id: 'mymap',
        map_opts: {
            center: [41.0, 69.0],
            zoom: 5,
            dragging: 0,
            zoomControl: 0
        }
    });

    (function init(s) {
        /**
         * Set up store bits which will be referenced later
         */
        s.opts = store_opts;
        s.map_id = store_opts.map_id || 'mymap';
        if (_.isNull(document.getElementById(s.map_id))) { console.error('Map ID not on the page: #', s.map_id); } // eslint-disable-line no-console
        s.map_element = $('#' + s.map_id);
        s.map = undefined; /* Holds the actual L.map instance for this Store */
        s.data = {}; /* Store auxiliary layer data */
        s.styles = _.defaults({}, s.styles, {
            normal: {
                fillColor: 'white',
                fillRule: 'nonzero',
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.0
            },
            hover: {
                weight: 5,
                color: '#222',
                fillColor: 'orange',
                fillRule: 'nonzero',
                dashArray: '',
                fillOpacity: 0.7
            },
            select: {
                weight: 5,
                color: '#222',
                fillColor: 'green',
                fillRule: 'nonzero',
                dashArray: '',
                fillOpacity: 0.7
            }
        });
        s.layers = s.layers || {};
        s.actions = {};
        s.features = {
            selected: [],
            hovered: []
        };
        s.event = [];
        s.controls = {};
    }(store));

    (function store_funcs(fn) {
        fn.map = function (opts) {
            var map_opts = _.defaults({}, opts, store.opts.map_opts);
            var m = L.map(store.map_id, map_opts);
            store.map = m;
            if (!map_opts.dragging) { m.dragging.disable(); m.keyboard.disable(); }
            if (!map_opts.controlZoom) { m.touchZoom.disable(); m.doubleClickZoom.disable(); m.scrollWheelZoom.disable(); }
            map_opts._initial_bounds = _.isUndefined(map_opts.bounds) ? undefined : JSON.parse(map_opts.bounds);
            if (!_.isUndefined(map_opts._initial_bounds)) { store.trigger('fitBounds', map_opts._initial_bounds); }
        };
        /**
         * Register a new Action which will be carried out on click / mouseover / mouseout event
         * See store.actions for functions which are triggered by this
         * @param opts
         */
        fn.addAction = function (opts) {
            /** Attach an "action" to a particular feature */
            /** "for geojson click: goto /en/dashboard/location/<%= code %>" */
            var defaults = {
                for: 'geojson', // Layer name
                name: 'click', // Action name
                action: 'go', // Do store.actions[action] when this action is called
                location: '/en/dashboard/location/<%= code %>' // Any other parameters to pass to store.action[action]
            };
            var action_opts = _.defaults({}, opts, defaults);

            var action = function (fn_opts) {
                var function_opts = _.defaults({}, fn_opts, action_opts);
                _.invoke(store.actions, [action_opts.action], function_opts);
            };
            store.event.push(_.defaults({}, action_opts, { fn: action }));
        };
        /**
         * Add a new Style to the store
         * @param opts
         * @returns {*}
         */
        fn.addStyle = function (opts) {
            /** This copies an object representing a Style to the styles which the map can address */
            /** Maybe subcless styles with an underscore? geojson_click ? */
            store.styles[opts.name] = opts;
            return store.styles[opts.name];
        };
        /**
         * Create a new TileLayer
         * @param layer_opts
         * @returns {*}
         */
        fn.addTileLayer = function (layer_opts) {
            var opts = _.defaults({}, layer_opts, {
                name: Math.random().toString(36).slice(2),
                url: 'http://(s).tile.osm.org/(z)/(x)/(y).png',
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                add: true
            }
            );

            var layer;
            var layer_name = opts.name || Math.random().toString(36).slice(2);
            /* Replace text surrounded by brackets with curly brackets
                Leaflet uses curly brackets for variables, just as Riot, which causes Riot to replace
                a string like '{s}' in the leaflet example with ''
             */
            var r = /(\()(\w)(\))/g;
            var url = opts.url.replace(r, '{$2}');
            layer = L.tileLayer(url, layer_opts);
            if (opts.zIndex) { layer.setZIndex(opts.zIndex); }
            store.layers[layer_name] = layer;

            if (opts.add) { store.map.addLayer(layer); }
            return store.layers[layer_name];
        };
        /**
         * Create a new GeoJSON layer
         * @param layer_opts
         * @returns {*}
         */
        fn.addGeoJsonLayer = function createGeoJsonLayer(layer_opts) {
            var layer;
            var opts = _.defaults(
                {},
                layer_opts,
                {
                    name: Math.random().toString(36).slice(2),
                    json_url: 'http://some-json-url',
                    add: 1,
                    data: []
                    // data_url: 'http://some-data-url',
                    // data_url: 'http://some-data-url',
                    // zIndex: 0,
                }
            );
            // If getJson or getData are undefined a completed Promise is returned
            var getJson = $.getJSON(opts.json_url);
            var getData = _.isUndefined(opts.data_url) ? $.when(opts.data) : $.getJSON(opts.data_url, opts.data_params || {});
            var layerPromise = $.when(getJson, getData);

            /** Expose Leaflet events to Riot's "observable" API
             * */
            function each(feature, this_layer) {
                /**
                 * Run any actions which filter to this layer name and action name
                 * @param e
                 */
                function runActions(e) {
                    _(store.event)
                        .filter({ for: opts.name, name: e.type })
                        .each(function (event_action) {
                            event_action.fn({ feature: feature, layer: this_layer });
                        });
                }

                this_layer.on({
                    mouseover: function (e) {
                        runActions(e);
                    },
                    mouseout: function (e) {
                        runActions(e);
                    },
                    click: function (e) {
                        runActions(e);
                    }
                });
            }

            /**
             * Create a geoJSON layer from a geographic source and a data source
             */
            layerPromise.done(function makeGeoJsonLayer(j, d) {
                if (!_.isUndefined(d) && d.length) {
                    _.each(j[0].features, function (feature) {
                        if (Object.prototype.hasOwnProperty.call(d[0], feature.id)) {
                            _.extend(feature.properties, d[0][feature.id]);
                        }
                    });
                }
                /**
                 * If a specific style is set for this layer it will be returned
                 * Otherwise the store's generic styles will be used
                 * @returns {*}
                 */
                function style() {
                    return _.clone(_.get(store.styles, ['layer_name', 'normal']) ||
                            _.get(store.styles, ['normal']) ||
                            _.get(store.styles, ['styles', 'normal'])
                    );
                }

                store.data[opts.name] = j[0];
                layer = L.geoJSON(j[0], {
                    style: style, //    _.get(tag.opts.styles, opts.style, tag.opts.styles.normal),
                    onEachFeature: each
                });

                store.layers[opts.name] = layer;
                if (opts.add) { store.map.addLayer(layer); }

                if (opts.zIndex) {
                    layer.setZIndex(opts.zIndex);
                }
                return opts;
            });

            return layerPromise;
        };
        /**
         * Wrapper around L.control
         * @param control_opts
         */
        fn.addControl = function (control_opts) {
            var opts = _.defaults(
                {},
                control_opts,
                {
                    name: Math.random().toString(36).slice(2),
                    template: '' +
                    '<h4> My Header </h4>' +
                    '<b> Something here </b> Hello World <br/>' +
                    '<p>And thats it for the template!</p>',
                    empty: 'No feature'
                }
            );

            var info = L.control();
            if (_.isString(opts.position)) {
                info.setPosition(opts.position);
            }


            info.onAdd = function () {
                this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
                if (opts.onclick) {
                    $(this._div).on('click', opts.onclick);
                }
                this.update();
                return this._div;
            };
            // method that we will use to update the control based on feature properties passed
            info.update = function (props) {
                if (props) {
                    this._div.innerHTML = _.template(opts.template)(props);
                    return;
                }
                this.clear();
            };

            info.clear = function () {
                this._div.innerHTML = opts.empty;
            };

            info.addTo(store.map);
            store.controls[opts.name] = info;
            return info;
        };

        fn.addToolTip = function (tool_opts) {
            var opts = _.defaults(
                {},
                tool_opts,
                {
                    name: Math.random().toString(36).slice(2),
                    template: '<p> <%= name %> </p>',
                    empty: 'No feature'
                }
            );
            var layer = store.layers[opts.for];
            layer.eachLayer(function (eachlayer) {
                eachlayer.bindTooltip(_.template(opts.template)(eachlayer.feature.properties));
            });
        };

        fn.setBounds = function (opts) {
            store.map.fitBounds(store.layers[opts.for].getBounds());
        };
    }(store.fn = store.fn || {}));

    (function (fn) {
        /**
         * Get a color from colorbrewer.js in the given palette, count and index
         */
        function getColour(palette, colour_count, colour_index) {
            /** To see valid palettes: _.keys(window.colorbrewer) */
            return _.get(window, ['colorbrewer', palette, colour_count, colour_index]);
        }

        function format(label, opts) {
            if (opts.legend_format === 'currency') {
                label = (Number(label)).toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 });
            } else if (opts.ceil) {
                label = _.ceil(label);
            } else if (_.isInteger(opts.precision)) {
                label = _.round(label, opts.precision);
            }
            return label;
        }

        /**
         * Set the color for a sinlge feature via either 'fillColor' or a lookup on colorbrewer.js
         * @param style_opts
         */
        function color_feature(style_opts) {
            var defaults = {
                fillOpacity: 0.5,
                fillRule: 'nonzero',
                // fillColor: 'blue', // Pass either fillColor or colorBrewer lookup
                brewer: {
                    palette: 'Blues',
                    count: 3,
                    index: 2
                }
            };
            var opts = _.defaults({}, defaults, style_opts);

            function getFeatureStyle(feature) {
                var currentStyle = _.invoke(store.layers[opts.for].options, 'style') || store.layers[opts.for].options.style;
                /* If 'opts' has a field parameter only features where this field is defined will have style changed */
                if (_.has(opts, 'field') && !_.has(feature.properties, opts.field)) {
                    return currentStyle;
                }
                return opts;
            }

            /* 'fillColor' takes precedence over a 'colorbrewer' lookup.  */

            if (!(opts.fillColor) && _.has(opts, ['brewer', 'palette']) && _.has(opts, ['brewer', 'index'])) {
                opts.fillColor = _.get(window, ['colorbrewer', opts.brewer.palette, opts.brewer.count, opts.brewer.index]);
            }
            store.layers[opts.for].setStyle(getFeatureStyle);
            L.Util.setOptions(store.layers[opts.for], { style: getFeatureStyle });
        }

        function chloropleth(style_opts) {
            var opts = _.defaults({}, style_opts, {
                classes: 5,
                palette: 'YlGn',
                add_legend: 'bottomright',
                precision: -5, // Round to a given number of decimal points
                ceil: false, // Round to the nearest whole number,
                legend_format: 'currency',
                zero_colour: 'gray', // Add a separate class for zero,
                no_data_label: 'No value'
            });
            var data = _.map(store.data[opts.for].features, 'properties');
            var field = opts.field;
            var colour_bucket_size;

            var max = _.max(_.map(data, field)) || 0;
            // var min = _.min(_.map(data, field)) || 0;
            var min = 0;
            var currentStyle;
            var legend;
            if (opts.zero_colour) { opts.classes -= 1; }
            if (max > min) {
                colour_bucket_size = ((max - min) / (opts.classes));
            } else {
                colour_bucket_size = 0;
            }

            colour_bucket_size = _.ceil(colour_bucket_size, opts.precision);

            if (opts.add_legend) {
                legend = L.control({ position: opts.add_legend });
                legend.onAdd = function () {
                    var div = L.DomUtil.create('div', 'map-info-box legend');
                    div.innerHTML += '<p><strong>' + opts.label || opts.field + '</strong></p>';
                    if (opts.zero_colour) {
                        div.innerHTML += '' +
                            '<i style="position:absolute; background:' + opts.zero_colour + '"></i>' +
                            '<span style="padding-left: 20px;">' + _.get(opts, 'no_data_label', format(0, opts)) + '</span>' +
                            '<br>';
                    }
                    _.each(_.range(opts.classes), function (c) {
                        var br = min + (c * colour_bucket_size);
                        var col = getColour(opts.palette, opts.classes, c);
                        var label = br + colour_bucket_size;

                        div.innerHTML += '' +
                            '<i style="position:absolute; background:' + col + '"></i>' +
                            '<span style="padding-left: 20px;">' + format(br, opts) + '&ndash;' + format(label, opts) + '</span>' +
                            '<br>';
                    });

                    return div;
                };

                legend.addTo(store.map);
            }

            currentStyle = _.invoke(store.layers[opts.for].options, 'style') || store.layers[opts.for].options.style;

            function getFeatureColor(feature) {
                var value = _.get(feature, ['properties', opts.field]);
                var colour;
                var opacity = 0.5;
                var colour_index = _.toInteger((value - min) / colour_bucket_size);
                if (colour_index > opts.classes - 1) { colour_index = opts.classes - 1; }
                if (opts.zero_colour && (value === 0 || _.isUndefined(value) || _.isNull(value))) {
                    colour = opts.zero_colour;
                } else {
                    colour = getColour(opts.palette, opts.classes, colour_index);
                }
                if (_.isUndefined(value)) {
                    opacity = 0;
                }
                return _.defaults({ fillOpacity: opacity, fillColor: colour }, currentStyle);
            }
            store.layers[opts.for].setStyle(getFeatureColor);
            L.Util.setOptions(store.layers[opts.for], { style: getFeatureColor });
        }

        fn.style = {
            chloropleth: chloropleth,
            color_feature: color_feature
        };
    }(store.fn = store.fn || {}));

    (function feature_actions(act) {
        /**
         * Zoom the map to a given feature
         * @param opts
         */
        act.zoom = function (opts) {
            store.map.fitBounds(opts.layer.getBounds());
        };
        /**
         * Change the window location based on a feature's properties
         * For instance, we can trigger a link to URL when a feature is clicked
         * @param opts
         */
        act.go = function (opts) {
            var compiled = _.template(opts.location);
            var url = compiled(opts.feature.properties);
            window.location = url;
        };
        /**
         * (re)set the style of a feature based on an action which happens over it
         * @param opts
         * @returns {*}
         */
        act.style = function (opts) {
            if (opts.style === 'reset') {
                return store.layers[opts.for].resetStyle(opts.layer);
            }
            return opts.layer.setStyle(opts.style);
        };
        /**
         * Update a leaflet control when a feature action occurs
         * @param opts
         * @returns {*}
         */
        act.update_control = function (opts) {
            if (opts.clear === true) {
                return store.controls[opts.control].clear();
            }
            return store.controls[opts.control].update(opts.feature.properties);
        };
    }(store.actions = store.actions || {}));
}
