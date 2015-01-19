var mapContext;

    function closest (num, arr) {
                var curr = arr[0];
                var diff = Math.abs (num - curr);
                for (var val = 0; val < arr.length; val++) {
                    var newdiff = Math.abs (num - arr[val]);
                    if (newdiff < diff) {
                        diff = newdiff;
                        curr = arr[val];
                    }
                }
                return curr;
        }

        var zoomFactors = {
            11 : 16,
            406 : 15,
            811 : 14,
            1609 : 13,
            3246 : 12,
            6492 : 11,
            12984 : 10,
            25968 : 9,
            51936 : 8,
            103872 : 7,
            207745 : 6
        };

        var zoomArr = Object.keys(zoomFactors);


        $('#storeMap').locationpicker({
            location: {latitude: 38.573631, longitude: -121.470021},   
            radius: 0.5 * 1609.34,  //Convert miles to meters
            inputBinding: {
                latitudeInput: $('#storeMap-lat'),
                longitudeInput: $('#storeMap-lon'),
                radiusInput: $('#storeMap-radius'),
                locationNameInput: $('#storeMap-address')
            },
            onchanged: function(currentLocation, radius, isMarkerDropped) {

               radius =  Math.round( radius * 1609.34); // Convert back to whole meters
               
               var closestNum = closest(radius, zoomArr);
               var zoomFactor = zoomFactors[closestNum];

               mapContext = $(this).locationpicker('map');
             //  google.maps.event.trigger(mapContext.map, "resize");
               mapContext.map.setZoom(zoomFactor);
            }
        });

        //Auto resize map for modal views!
        $('#locationSettingsModal').on('shown.bs.modal', function () {
                $('#storeMap').locationpicker('autosize');
        });


        $("#saveLocationSettings").click(function() {

                var newLocationMap = $('#storeMap').locationpicker('map').map;

                var newRadius = $('#storeMap-radius').val();

                var populationOptions = {
                          strokeColor: '#FF0000',
                          strokeOpacity: 0.8,
                          strokeWeight: 2,
                          fillColor: '#FF0000',
                          fillOpacity: 0.15,
                          map: map,
                          center: new google.maps.LatLng(newLocationMap.getCenter().k, newLocationMap.getCenter().D),
                          radius: parseInt(newRadius) * 1609.344
                    };

                alert(newRadius);

                var mapOptions = {
                    zoom: 13,
                    center: new google.maps.LatLng(newLocationMap.getCenter().k, newLocationMap.getCenter().D),
                  }

                var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

                centerMarker = new google.maps.Marker({
                        position: new google.maps.LatLng(newLocationMap.getCenter().k, newLocationMap.getCenter().D),
                        map: map,
                        icon: 'https://maps.google.com/mapfiles/kml/shapes/schools_maps.png'
                });

                // Add the circle for this city to the map
                cityCircle = new google.maps.Circle(populationOptions);



        });






