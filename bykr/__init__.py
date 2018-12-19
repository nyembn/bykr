import os

from flask import Flask
from datetime import timedelta

'''def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)'''
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev')
    app.permanent_session_lifetime = timedelta(minutes=10)

    from . import db
    #db.init_app(app)
    #are you allowed to pass it this way? yes
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import user_tasks
    app.register_blueprint(user_tasks.bp)

    from . import profile
    app.register_blueprint(profile.bp)


    return app
