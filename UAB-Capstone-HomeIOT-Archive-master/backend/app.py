# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

import os

# Import flask
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Import SQL ORM and database extension
from flask_sqlalchemy import SQLAlchemy
from extensions.database import db
from models.location import Location
from models.device import Device
from models.eventlog import EventLog
from models.usage import Usage

# Import API definitions/views
from views.api import apiv1
from views.locations import api as locationApi
from views.devices import api as deviceApi
from views.usage import api as usageApi

# Load PostgreSQL Config
import yaml

def register_extensions(app):
    db.init_app(app)


def create_app(pgconfig):
    print("HELLO")
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    app.register_blueprint(apiv1)

    if pgconfig is not None:
        # If pgconfig is specified attempt to connect to the db
        DB_URI = 'postgres://%(user)s:%(password)s@%(ip)s:%(port)s/%(database)s' % pgconfig

        print(DB_URI)
        app.config["SQLALCHEMY_ECHO"] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        # If no pgconfig given default to local sqlitedb
        # TODO: For ease of development locally, I am using SQLite temporarily. This will change to Postgre in the future.
        app.config["SQLALCHEMY_ECHO"] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "homeiot.db")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    app.wsgi_app = ProxyFix(app.wsgi_app)

    register_extensions(app)

    return app


if __name__ == "__main__":
    with open("./pgconfig.yml", 'r') as stream: 
        try:
            pgconfig = yaml.safe_load(stream)
            app = create_app(pgconfig)
            app.run(debug=True)
        except yaml.YAMLError as exc:
            print(exc)
