// Update score and return results on .vote event
$('.vote').click(function() {
    element = $(this); // Element event handler bound to
    $.ajax({
        url: '/poll/' + $(this).data('poll-id') + '/vote/' + $(this).data('vote'),
        data: {resp_id: $(this).data('resp-id')},
        type: 'POST',
        success: function(response) {
            // Update total score
            element.parent().parent().parent().find('.score').html(response['score']);
            // Update up-vote and down-vote scores
            element.parent().parent().find('.up-score span').html(response['up']);
            element.parent().parent().find('.down-score span').html(response['down']);
        },
        error: function(error) {
            console.log(error);
        }
    });
});
