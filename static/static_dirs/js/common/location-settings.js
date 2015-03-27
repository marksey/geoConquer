var mapContext;
var allMarkers = {};
var map;

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
            location: {latitude: 34.052234, longitude: -118.243685},   
            radius: 1 * 1609.34 / 1.6,  //Convert miles to meters
            inputBinding: {
                latitudeInput: $('#storeMap-lat'),
                longitudeInput: $('#storeMap-lon'),
                radiusInput: $('#storeMap-radius'),
                locationNameInput: $('#storeMap-address')
            },
            onchanged: function(currentLocation, radius, isMarkerDropped) {

               radius =  Math.round( radius * 1609.34 / 1.6); // Convert km back to whole meters
               
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
                $("#radius").html($('#storeMap-radius').val()); 
                reDrawTweetsOnRadiusChange($('#storeMap-radius').val());
            }


        });

        $('#autoFavorite').click(function(e) {

            e.preventDefault();


            for (var tag in allMarkers)
            { 
                for (var markerIndex in allMarkers[tag]) {
                    ajaxFavoriteTweet(allMarkers[tag][markerIndex].metadata.tweet_id);
                }
            }
        });



        function reDrawTweetsOnRadiusChange(radius)
        {
            var map = $('#storeMap').locationpicker('map').map;
            var centerCoordinates = map.getCenter().toString().substring(1, map.getCenter().toString().length - 1);
            var tags = $.map(allMarkers, function(element,index) {return index});

            for (var tag in tags)
            {
                console.log("Removing: " + tags[tag]);
                removeMarkers(tags[tag]);
                removeUsers(tags[tag]);
                geoSearchByTag(tags[tag], centerCoordinates, radius);   
            }


        }



  






