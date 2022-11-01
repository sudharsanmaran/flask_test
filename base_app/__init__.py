import os
from flask import Flask
from . import db


def create_app(test_config=None):
    app = Flask('base_app', instance_relative_config=True)

    db.init_app(app)
    app.config.from_file()

    @app.route('/')
    def is_ok():
        return 'OK'

    return app
