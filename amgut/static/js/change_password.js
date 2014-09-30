function validatePassRequest() {
    for(var i = 0; i < document.resetpass_request.length; i++) 
    {
        document.resetpass_request[i].className = document.resetpass_request[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
    
    var valid = true;
    
    if(!validateEmail(document.resetpass_request.email.value))
    {
        document.resetpass_request.email.className += " highlight"
        valid = false;
    }
    if(document.resetpass_request.email.value == "")
    {
        document.resetpass_request.email.className += " highlight"
        valid = false;
    }
    if(document.resetpass_request.kit_id.value == "")
    {
        document.resetpass_request.kit_id.className += " highlight"
        valid = false;
    }
    if(valid)
        $('#resetpass_request').submit();
}

function validatePasswords()
{
    var valid = true;
    if(! (document.reset_password.confirm_password.value == document.reset_password.new_password.value))
    {
        document.reset_password.confirm_password.className += " highlight"
        valid = false;
    }    
    if(valid)
        $('#reset_password').submit();
}

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