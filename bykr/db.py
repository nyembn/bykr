import os
import click
import mysql.connector
from flask import current_app, g
from flask.cli import with_appcontext

# These environment variables are configured in app.yaml.
#CLOUDSQL_CONNECTION_NAME = current_app.config['CLOUDSQL_CONNECTION_NAME']
'''
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'hello1234'
CLOUDSQL_CONNECTION_NAME = 'bykrblog:us-central1:bykrblogdb'
'''
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

def get_db():
    if 'db' not in g:
 # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
            cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

            '''g.db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD, db='bblog')'''
            g.db = mysql.connector.connect(unix_socket=cloudsql_unix_socket, user='root', passwd='hello1234', db='bblog')
        else:
            g.db = mysql.connector.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db='bblog')


    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
'''
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


#@click.command('init-db')
#@with_appcontext
def startup_db():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    #app.cli.add_command(init_db_command)
    startup_db()

import os

import MySQLdb
import webapp2
from flask import current_app, g
from flask.cli import with_appcontext


        ###########db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db


class MainPage(webapp2.RequestHandler):
    def get(self):
        """Simple request handler that shows all of the MySQL variables."""
        self.response.headers['Content-Type'] = 'text/plain'

        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')

        for r in cursor.fetchall():
            self.response.write('{}\n'.format(r))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
'''

