$(document).ready(function(){
    $('a.expand_card').on('click', function(){
        $('.collapse_card').collapse('toggle');
    });
    
    // replace single activity
    $('#btn-replace').on('click', function() {
        var clicked = $(this);
        
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            success: function(){
                $('#confirmModal').modal('hide');
                insertMessage('Replace Succeeded', 'success');
            },
            error: function(data){
                $('#confirmModal').modal('hide');
                insertMessage('Replace Failed', 'warning');
            }
        });
    });
});

function insertMessage( text, type ){
    var className = 'message bold text-' + type + ' btn-' + type ;
    var pMessage = $( '<p />' ).addClass( className )
                                .css( 'padding', '10px' )
                                .html( text );
    setTimeout(
        function()
        {
            pMessage.remove();
        },
        10 * 1000
    );
    $('#ajax_messages').append(pMessage);
}
