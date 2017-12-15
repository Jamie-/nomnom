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
            // Update up-vote, down-vote and flag-vote scores
            element.parent().parent().find('.up-score span').html(response['up']);
            element.parent().parent().find('.down-score span').html(response['down']);
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// Share button popover
$('#share').popover({
    placement: 'bottom',
    template: '<div class="popover share-popover" role="tooltip"><div class="arrow"></div><div class="pop-header"><h3 class="popover-header"></h3><button class="float-right">&times;</button></div><textarea class="popover-body"></textarea></div>'
});
