# Contributor(s): Adrian Gose, Senay Patel
# If you worked on this file, add your name above so we can keep track of contributions

# This file is meant to be called via CLI interface
# and is designed to aid in creating database tables and
# mock data. Do not import this generator into any modules.

# Misc Imports
import os
from datetime import datetime, timedelta
from datetime import date as dt
import random
import calendar

# Import SQL Models
from models.location import Location
from models.device import Device
from models.eventlog import EventLog
from models.usage import Usage
from data_generator.weather_data import *

# Import DAO Helpers
# If you don't know, DAO = Data Access Object
import dao.location as ldao
import dao.device as ddao
import dao.events as edao
import dao.usage as udao
from dao.calculate import *

# Import DB instance
from app import create_app
from extensions.database import db

# PostgreSQL config
import yaml
pgconfig = None
with open("./pgconfig.yml", 'r') as stream: 
    try:
        pgconfig = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

app = create_app(pgconfig)
db.init_app(app)

if __name__ == "__main__":
    # Delete SQLITE DB
    # SQLITE ONLY FOR DEBUG/DEV PURPOSES. PRODUCTION MUST USE
    # UAB POSTGRES
    # TODO: Connect PostgreSQL
    basedir = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(os.path.join(basedir, "homeiot.db")):
        os.remove(os.path.join(basedir, "homeiot.db"))

    # Run this file directly to create the database tables.
    print("Connecting to Database")

    # Create application context and perform database initialization queries within the context
    with app.app_context():
        print("DB Connected. Generating tables...")
        db.drop_all(bind=None)
        print("Tables removed. Ready to run generator...")

       


