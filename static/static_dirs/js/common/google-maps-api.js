var allMarkers = {};
var allUsers = {};
var numberOfTweets = 0;
var map;
var infowindow, marker;
var myLatitude = 38.575655;
var myLongitude = -121.480336;


var rad = function(x) {
          return x * Math.PI / 180;
};

function calculateDistance(lat1, lon1, lat2, lon2){

            var radiusEarth = 3959;
            var dlon = rad(parseFloat(lon2) - lon1);
            var dlat = rad(parseFloat(lat2) - lat1);
            var a = Math.pow(Math.sin(dlat / 2.0), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(dlon / 2.0), 2);
            var c = 2 * Math.atan2( Math.sqrt(a), Math.sqrt(1 - a) );
            var d = radiusEarth * c;  
            return d;

}

function removeMarkers(tag) {


    for(var i=0; i < allMarkers[tag].length; i++)
    {
        var marker = allMarkers[tag][i];
        marker.setMap(null);
    }

    numberOfTweets -= allMarkers[tag].length ;
    $("#totalTweeters").html(numberOfTweets);

    delete allMarkers[tag]; 

}

function removeUsers(tag) {

    delete allUsers[tag];

}

function getAllTweetsInRadius()
{
    var usersToFollow = [];

    $.each( allUsers, function( tag, user ) {
      
        usersToFollow.push(user);
      
    });

    console.log("To follow: " + usersToFollow);


}



function drawTweets(q, local_tweets, centerCoords, radiusFromCenter) {

            myLatitude = parseFloat(centerCoords.split(',')[0]);
            myLongitude = parseFloat(centerCoords.split(',')[1]);

            radiusFromCenter = Math.round(parseFloat(radiusFromCenter))

            allMarkers[q] = [];
            allUsers[q] = [];

            var map = $('#storeMap').locationpicker('map').map;
            var infowindow = new google.maps.InfoWindow({ maxWidth: 300 });
            console.log("Num tags" + Object.keys(allMarkers).length);

             //alert("There are " + local_tweets.length + " tweets");

             for (var i = 0; i < local_tweets.length; i++) { 


                var milesAway = calculateDistance(myLatitude, myLongitude, local_tweets[i]['latitude'], local_tweets[i]['longitude']);

                milesAway = Math.round(milesAway * 10) / 10;   //Round to the nearest tenth

                var tweetUrl = 'http://www.twitter.com/' + local_tweets[i]['screen_name'] + '/status/' + local_tweets[i]['tweet_id'];

                //Don't include those outside radius
                if (milesAway > radiusFromCenter) continue;


                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(local_tweets[i]['latitude'], local_tweets[i]['longitude']),
                    map: map,
                    animation: google.maps.Animation.DROP
                });

                marker.metadata = {tweet_id: local_tweets[i]['tweet_id']};

                if (local_tweets[i]['favorited']) 
                {
                    marker.setIcon('http://google-docslist-gadget.googlecode.com/svn-history/r91/trunk/images/icon-star-big.gif');   
                }

                allMarkers[q].push(marker);
                allUsers[q].push(local_tweets[i]['screen_name']);

                console.log(marker);

                google.maps.event.addListener(marker, 'click', (function(marker, i) {

                    return function() {

                         console.log("Screen name: " + local_tweets[i]['screen_name'] + " TWEET ID: " + local_tweets[i]['tweet_id'] + " favorited: " + local_tweets[i]['favorited'] + "\n");

                         var contentString = '<div id="content">' + 
                                                '<div id="siteNotice"></div>'+
                                                '<h3 id="firstHeading" class="firstHeading">'  +
                                                    '<img alt="image" height="10%" width="10%" class="img-circle" src="' + local_tweets[i]['profile_image_url'] + ' ">&nbsp;' +
                                                    '<a target="_blank" class="profileHeader" href="http://www.twitter.com/' + local_tweets[i]['screen_name'] + '" target="_blank">@' + local_tweets[i]['screen_name'] +
                                                    '</a>'+
                                                '</h3>'+
                                                '<div id="bodyContent">'+
                                                    '<p><b>' + local_tweets[i]['tweet_text'] + '</b></p>' +
                                                    '<p>' +
                                                        '<b>' + 
                                                            '<i class="fa fa-clock-o"></i>&nbsp;' + local_tweets[i]['time_since_tweet'] +  
                                                            '<i class="fa fa-map-marker"></i> ' + milesAway + ' mi away ' + 
                                                        '</b>' +
                                                        '<span class="pull-right">' +
                                                                '<a target="_blank" href="' + tweetUrl + '" class="fa fa-mail-reply" data-toggle="modal">&nbsp;&nbsp;&nbsp;&nbsp;</a>' +
                                                                '<a href="#" class="fave fa fa-star" data-tweet-id="' + local_tweets[i]['tweet_id'] + '" data-toggle="tooltip" data-placement="right" title="" data-original-title="Tooltip on right" onclick="ajaxFavoriteTweet(this); return false;"></a>' +
                                                                '<a href="#" class="fa fa-user" data-tweet-id="' + local_tweets[i]['tweet_id'] + '" data-toggle="tooltip" data-placement="right" title="" data-original-title="Tooltip on right" onclick="followUser(this); return false;" style="margin-left: 12px;"></a>' +
                                                        '</span>' + 
                                                    '</p>'+
                                                '</div>'+
                                            '</div>';

                      infowindow.setContent(contentString);
                      infowindow.open(map, marker);
                    }
                  })(marker, i));
            }



                (function() {
                   // your page initialization code here
                   // the DOM will be available here

                    //Remove Google Maps Marker infoWindow scrolling
                    google.maps.event.addListener(infowindow, 'domready', function() {
                        $('#content').parent().parent().css('overflow', 'hidden');
                        $('#content').parent().parent().css('min-width', '200px');
                        $('#content').parent().parent().css('line-height', '1.35');
                    });


                })();
    }

function geoSearchByTag(q, centerCoords, radiusFromCenter){

            
    $.ajax({
        url : "/json_local_tweets/", // the endpoint
        type : "GET", // http method
        datatype: 'json',
        data: {
                coords : centerCoords.replace(/\s/g, ''),
                radius : Math.round(parseFloat(radiusFromCenter)),
                q: q 
            },
        // handle a successful response
        success : function(local_tweet_results) {

            drawTweets(q, local_tweet_results, centerCoords, radiusFromCenter);
            numberOfTweets += local_tweet_results.length;
            $("#totalTweeters").html(numberOfTweets);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
         
            alert(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }

    });
}

function ajaxFavoriteTweet(obj) {

    var tweet_id;

    try{
     tweet_id = obj.getAttribute("data-tweet-id");
    } 
    catch(err) {
     tweet_id = obj;
    }

    console.log("Ajax: " + tweet_id);

    $.ajax({
        url : "/favorite_tweet/", // the endpoint
        type : "GET", // http method
        datatype: 'json',
        data: {
                tweet_id : tweet_id,
            },
        // handle a successful response
        success : function(response) {

                if (response)
                {
                    var favoritedMarker = getFavoritedMarker(tweet_id);
                    favoritedMarker.setIcon('http://google-docslist-gadget.googlecode.com/svn-history/r91/trunk/images/icon-star-big.gif');   
                } 
                else
                {
                    alert("You already favorited this tweet!");
                }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
         
            alert(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }

    });

    return false;
}

function getFavoritedMarker(tweet_id)
{
    for (var tag in allMarkers) 
    {    
        for (var marker in allMarkers[tag]) 
            { 
                if (tweet_id == allMarkers[tag][marker].metadata.tweet_id)
                {
                    return allMarkers[tag][marker]
                }
            } 
    }

}



