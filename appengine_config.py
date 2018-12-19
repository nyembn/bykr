import os
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('venv27/lib')
#vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv27/lib'))
#vendor.add('/home/beautiful/works/Python/flask-tutorial/venv27/lib')
