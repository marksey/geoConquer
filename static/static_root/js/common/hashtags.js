window.onload = function(){
    // x functionality when window loads


    //Allow Enter keystroke to add tag 
     $('#inpAddTags').keypress(function(e) {
        
        //On enter hit click and reset input
        if (e.which == '13') {
            $('#addTag').click();
            $("#inpAddTags").val("");
        }
    });
    

    //Adding tags one at a time
    $('#addTag').click(function() {
       
       
       var tag = $('#inpAddTags').val();
        
       var newTagElement = '<span class="unit-tag" data-tag="' + tag  + '" data-id="278913968">'+
                        '<span>'  +  tag +  '</span>' + 
                        '<a href="#" class="delete" tabindex="-1">x</a>' +
                    '</span>';
            
        $('#tagBody').append(newTagElement);

        //var map = $('#storeMap').locationpicker('map').map;
       alert("yes");
       // var centerCoordinates = map.getCenter().toString().substring(1, map.getCenter().toString().length - 1);
        geoSearchByTag(tag, centerCoordinates);

    });
    
    //Removing tags one at a time
     $(document).on("click", ".delete", function(e) {
        
        e.preventDefault();
        var tag = $(this).parent().text().slice(0,-1);
        removeMarkers(tag);
        $(this).parent().remove();
        
    });

   



}
    


