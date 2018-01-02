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
            // Show arrow as pressed
            if (response['up'] === 1) {
                element.find('i').addClass('upvote');
            } else {
                element.find('i').removeClass('upvote');
                //TODO Clear style on down-vote icon
            }
            if (response['down'] === 1) {
                element.find('i').addClass('downvote');
            } else {
                element.find('i').removeClass('downvote');
                //TODO Clear style on up-vote icon
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// Flag a poll
$('.poll-flag').click(function () {
   element = $(this);
   $.ajax({
        url: '/poll/' + $(this).data('poll-id') + '/vote/' + $(this).data('vote'),
        data: {resp_id: $(this).data('resp-id')},
        type: 'POST',
        success: function(response) {
            // Show flag button as pressed
            element.find('i').addClass('flag-active');
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// Share button popover
$('#share').popover({
    html: true,
    placement: 'bottom',
    title: 'Share this poll!<span class="close">&times;</span>',
    content: function() {
        return '<input id="sharelink" type="text" size="30" data-trigger="manual" readonly onclick="copyToClip(this)" value="' + $(this).data('share-url') + '">';
    }
}).on('shown.bs.popover', function() {
    // Add listener for close button
    $('.close').click(function() {
        $(this).parents('.popover').popover('hide');
    });
});

// Copy sharing link to clipboard
function copyToClip(element) {
    element.focus();
    element.select();
    var success = document.execCommand('copy');
    var resp = success ? 'Copied!' : 'Unable to copy :(';
    // Show tooltip for 0.5s
    $(element).tooltip('hide').attr('data-title', resp).tooltip('show');
    setTimeout(function() {
        $(element).tooltip('hide');
    }, 500);
}
