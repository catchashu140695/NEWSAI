$(document).ready(function () {

    eel.expose(DisplayStatus)
    function DisplayStatus(message) {       
        str = '<p>' + message + '</p>';
        $('.siri-status').html(str);
    
        // Hide the message after 5 seconds
        setTimeout(function() {
            $('.siri-status p').fadeOut('slow', function() {
                $(this).remove();
            });
        }, 5000); // 5000 milliseconds = 5 seconds
    }

    eel.expose(DisplayMessage)
    function DisplayMessage(message, actor="AI") {
        var str = $('.siri-message').html();
        if (actor == "AI") {
            str += '<div class="row" style="border-radius: 10px;">';
            str += '<div class="col-md-12 text-left">';           
            str += '<span style="font-weight:600;">Bot : '+message+'</span>';
            str += '</div>';
            str += '</div>';
            str += '</br>';
           

        }
        else {
            str += '<div class="row" style="border-radius: 10px;">';
            str += '<div class="col-md-12 text-right">';           
            str += '<span style="font-weight:600;">User : '+message+'</span>';
            str += '</div>';
            str += '</div>';
            str += '</br>';
            
        }
        $('.siri-message').html(str)

    }

    eel.expose(showhood)
    function showhood() {
        $('#Oval').attr('hidden', false);
        $('#SiriWave').attr('hidden', true);
    }


});