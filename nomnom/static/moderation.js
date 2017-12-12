// Update score and return results on .vote event
$('.vote').click(function() {
    element = $(this); // Element event handler bound to
    $.ajax({
        url: '/admin/moderation/' + $(this).data('poll-id') + '/action/' + $(this).data('vote'),
        data: {resp_id: $(this).data('resp-id')},
        type: 'POST',
        success: function(response) {
            // Update total score
            element.parent().parent().remove();
        },
        error: function(error) {
            console.log(error);
        }
    });
});
