import event

# Application wide events
poll_created_event = event.Event()
poll_deleted_event = event.Event()
response_event = event.Event()
vote_event = event.Event()
auto_moderated_poll_event = event.Event()
auto_moderated_response_event = event.Event()
flagged_nomnommodel_event = event.Event()
