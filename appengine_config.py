
"""This file is loaded when the app starts."""

import os

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'handlers'))
# vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/models'))
# vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/validate'))
