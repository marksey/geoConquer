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
            radius: 1 * 1609.34,  //Convert miles to meters
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

        
        $('#storeMap-radius').keypress(function(e) {

            //On enter hit click and reset input
            if (e.which == '13') {
            }

        });

        $('#autoFollow').click(function(e) {

            e.preventDefault();
            getAllTweetsInRadius();
        });



  






