

"""
This file contains all of the configuration values for the application.
Update this file with the values for your specific Google Cloud project.
You can create and manage projects at https://console.developers.google.com
"""

import os

# The secret key is used by Flask to encrypt session cookies.
#SECRET_KEY = 'b\xa8\x15\x1a\xea\x1a\r\x88\xdeT\xac\xf4\x95]R\xce\x0c'

# There are three different ways to store the data in the application.
# You can choose 'datastore', 'cloudsql', or 'mongodb'. Be sure to
# configure the respective settings for the one you choose below.
# You do not have to configure the other data backends. If unsure, choose
# 'datastore' as it does not require any additional configuration.
DATA_BACKEND = 'cloudsql'

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'bykrblog'

# CloudSQL & SQLAlchemy configuration
# Replace the following values the respective values of your Cloud SQL
# instance.
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'hello1234'
CLOUDSQL_DATABASE = 'bykrblg'
# Set this value to the Cloud SQL connection name, e.g.
#   "project:region:cloudsql-instance".
# You must also update the value in app.yaml.
CLOUDSQL_CONNECTION_NAME = 'bykrblog:us-central1:bykrblg'

# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.

# Alternatively, you could use a local MySQL instance for testing.
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)
#where this is defined
if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

# Mongo configuration
# If using mongolab, the connection URI is available from the mongolab control
# panel. If self-hosting on compute engine, replace the values below.
MONGO_URI = 'mongodb://user:password@host:27017/database'
