# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def commit(commitobject):
    db.session.add(commitobject)
    db.session.commit()