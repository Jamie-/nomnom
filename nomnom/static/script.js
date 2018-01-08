// Update score and return results on .vote event
$(document).on('click', '.vote', function() {
    element = $(this); // Element event handler bound to
    $.ajax({
        url: '/poll/' + $(this).data('poll-id') + '/vote/' + $(this).data('vote'),
        data: {resp_id: $(this).data('resp-id')},
        type: 'POST',
        success: function(response) {
            // Update total score
            var score = element.parent().parent().find('.score');
            if (score.length !== 0) {
                score.html(response['score']);
            } else {
                element.parent().parent().parent().find('.score').html(response['score']);
            }
            // Update up-vote, down-vote and flag-vote scores
            element.parent().parent().find('.up-score span').html(response['up']);
            element.parent().parent().find('.down-score span').html(response['down']);
            // Show arrow as pressed when clicked
            if (element.data('vote') === "resp-up") {
                if (element.find('i').hasClass('upvote'))
                    element.find('i').removeClass('upvote');
                else
                    element.find('i').addClass('upvote');
                element.parent().parent().find('.down-score i').removeClass('downvote');
            } else {
                element.find('i').removeClass('upvote');
            }
            if (element.data('vote') === "resp-down") {
                if (element.find('i').hasClass('downvote'))
                    element.find('i').removeClass('downvote');
                else
                    element.find('i').addClass('downvote');
                element.parent().parent().find('.up-score i').removeClass('upvote');
            } else {
                element.find('i').removeClass('downvote');
            }
            // Show flag as pressed when clicked
            if (element.data('vote') === "resp-flag") {
                element.find('i').addClass('flag-active');
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// Flag a poll
$(document).on('click', '.poll-flag', function() {
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

$(window).on('resize', function(){
    $('#poll-list .card').css('margin',$(window).width()*0.008);
    if ($(window).width() > 1500){
		$('#poll-list .card').width(1500/3 - 1500*0.05);
		$('#poll-list .card').css('margin',1500*0.008);
	} else if ($(window).width() > 1350){
		$('#poll-list .card').width($(window).width()/3 - $(window).width()*0.03);
	} else if ($(window).width() < 950){
		$('#poll-list .card').width($(window).width() - $(window).width()*0.1);
	} else {
		$('#poll-list .card').width($(window).width()/2 - $(window).width()*0.06);
	}
}).resize();
