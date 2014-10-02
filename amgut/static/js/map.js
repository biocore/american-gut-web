$(document).ready(function(){

    $("ul.subnav").parent().append("<span></span>"); //Only shows drop down trigger when js is enabled - Adds empty span tag after ul.subnav

    $("ul.topnav li span").click(function() { //When trigger is clicked...

        //Following events are applied to the subnav itself (moving subnav up and down)
        $(this).parent().find("ul.subnav").slideDown('fast').show(); //Drop down the subnav on click

        $(this).parent().hover(function() {
        }, function(){
            $(this).parent().find("ul.subnav").slideUp('slow'); //When the mouse hovers out of the subnav, move it back up
        });

        //Following events are applied to the trigger (Hover events for the trigger)
        }).hover(function() {
            $(this).addClass("subhover"); //On hover over, add class "subhover"
        }, function(){  //On Hover Out
            $(this).removeClass("subhover"); //On hover out, remove class "subhover"
    });

});

function toggleSection(section_name)
{
    div = document.getElementById(section_name);
    header_name = section_name + '_header';
    if (div.style.display == 'none')
    {
        $('#' + section_name).fadeIn('fast')
        header_content = $('#' + header_name)[0].innerHTML
        $('#' + header_name)[0].innerHTML = header_content.replace('+', '-');
        window.scrollBy(0, 200);
    }
    else
    {
        $('#' + section_name).fadeOut('fast')
        header_content = $('#' + header_name)[0].innerHTML
        $('#' + header_name)[0].innerHTML = header_content.replace('-', '+');
    }
}

function drawMap(zoom_level, position)
{
    var mapOptions =
    {
        zoom: zoom_level,
        center: position,
        scrollwheel: false,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        mapTypeControl: false,
        streetViewControl: false,
        panControl: false
    };


    var stylez = [
        {
          featureType: "all",
          elementType: "all",
          stylers: [
            { saturation: -100 } // <-- THIS
          ]
        }
    ];

    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

    var mapType = new google.maps.StyledMapType(stylez, { name:"Grayscale" });
    map.mapTypes.set('tehgrayz', mapType);
    map.setMapTypeId('tehgrayz');

    setMarkers(map, latlongs_db);
}

function renderLocalizedMap(position)
{
    p = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    zoom_level = 10;
    drawMap(zoom_level, p);
}

function renderMap()
{
    p = new google.maps.LatLng(LAT, LONG);
    zoom_level = ZOOM;
    drawMap(zoom_level, p);
}

function initialize()
{
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(renderLocalizedMap, renderMap);
    }
    else
    {
        renderMap()
    }
}

function setMarkers(map, locations)
{
    for (var i = 0; i < locations.length; i++)
    {
        var loc = locations[i];
        var myLatLng = new google.maps.LatLng(loc[0], loc[1]);

        var pinColor = loc[2];
        var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=wc-male|" + pinColor,
            new google.maps.Size(21, 34),
            new google.maps.Point(0,0),
            new google.maps.Point(10, 34));
        var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
            new google.maps.Size(40, 37),
            new google.maps.Point(0, 0),
            new google.maps.Point(12, 35));

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            icon: pinImage,
            shadow: pinShadow
        });
    }
}

window.onload=initialize;
