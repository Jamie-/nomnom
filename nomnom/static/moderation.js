// Approve/remove flagged polls and responses
$('.vote').click(function() {
    element = $(this); // Element event handler bound to
    $.ajax({
        // post to the moderation URL
        // cookies are checked on ajax, so only admins can access this
        url: '/admin/moderation/' + $(this).data('poll-id') + '/action/' + $(this).data('vote'),
        data: {resp_id: $(this).data('resp-id')},
        type: 'POST',
        success: function(response) {
            // remove the element from the table
            element.parent().parent().remove();
        },
        error: function(error) {
            console.log(error);
        }
    });
});
