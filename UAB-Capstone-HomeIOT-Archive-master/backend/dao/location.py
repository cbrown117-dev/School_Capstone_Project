# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions
from typing import List

from models.location import Location
from extensions.database import db, commit


def add_location(name) -> Location:
    """

    :param name:
    :return:
    """
    newloc = Location(name)
    commit(newloc)
    return newloc

def get_location_by_name(name: str) -> Location:
    """

    :param name:
    :return:
    """
    return Location.query.filter(Location.name.ilike(name)).first()


def get_locations() -> List[Location]:
    """

    :return:
    """
    return Location.query.all()