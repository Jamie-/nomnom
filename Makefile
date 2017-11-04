.DEFAULT_GOAL := run
.PHONY: clean, depends, run, deploy, cloud-logs, view

# This will need changing to wherever you installed your GCloud SDK - please don't commit changes to this line though!
gcloud-sdk = /C:/Program\ Files\ \(x86\)/Google/Cloud\ SDK/google-cloud-sdk

clean: # Clean build files
	rm -rf *.pyc
	rm -rf __pycache__/
	rm -rf **/__pycache__/

depends: # Install all dependancies into `lib`
	pip install -t lib -r requirements.txt

run: # Run app locally
	/usr/bin/env python $(gcloud-sdk)/platform/google_appengine/dev_appserver.py --host 127.0.0.1 .

deploy: # Deploy app to AppEngine
	gcloud app deploy --quiet

cloud-logs: # Watch AppEngine cloud logs
	gcloud app logs tail -s default

view: # Open deployed app in browser
	gcloud app browse
