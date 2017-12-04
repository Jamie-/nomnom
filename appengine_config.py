"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os.path
# add `lib` subdirectory to `sys.path`, so our `main` module can load third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

if os.name == 'nt':
    os.name = None
    sys.platform = ''

# Tagging library import for GAE
import os
if 'Google App Engine' in os.environ['SERVER_SOFTWARE']:
    from google.appengine.ext import vendor
    vendor.add('gae_lib') # Add any libraries install in the "lib" folder.
