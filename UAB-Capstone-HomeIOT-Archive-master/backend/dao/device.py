# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from typing import List

from models.device import *
from models.location import *
from extensions.database import commit


###############
# Lights
###############
def add_light(location: Location, x: int, y: int, name: str, wattage: int) -> Light:
    """
    Adds a light to devices table and returns a Light model

    :param name:
    :param wattage:
    :param location:
    :return:
    """
    newlight = Light(location, x, y, name, wattage)
    commit(newlight)
    return newlight


def get_lights() -> List[Light]:
    return Light.query.all()


###############
# Doors
###############
def add_door(location: Location, x: int, y: int, name: str) -> Door:
    """
    Adds a door to devices table and returns a Door model

    :param location: The location to add the door to
    :param name: A unique name for the door
    :return: Door object
    """
    door = Door(location, x, y, name)
    commit(door)
    return door


def get_doors() -> List[Door]:
    """
    Gets a List of Door objects

    :return: List[Door]
    """
    return Door.query.all()


###############
# Windows
###############
def add_window(location: Location, x: int, y: int, name: str) -> Window:
    """
    Adds a window to devices table and returns a Window model

    :param location:
    :param name:
    :return:
    """
    newlight = Window(location, x, y, name)
    commit(newlight)
    return newlight


def get_windows() -> List[Window]:
    """

    :return:
    """
    return Window.query.all()


###############
# Water
###############
def add_water_meter(location: Location, x: int, y: int, name: str) -> Water:
    """
    Adds a water meter to devices table and returns a Water model

    :param location:
    :param name:
    :return:
    """
    newlight = Water(location, x, y, name)
    commit(newlight)
    return newlight


def get_water_meters() -> List[Water]:
    return Water.query.all()


###############
# Generic Electric Device
###############
def add_electric_device(location: Location, x: int, y: int, name: str, wattage: int) -> Electric:
    """

    :param location:
    :param name:
    :param wattage:
    :return:
    """
    newelec = Electric(location, x, y, name, wattage)
    commit(newelec)
    return newelec


def get_electric_devices() -> List[Electric]:
    """

    :return:
    """
    return Electric.query.all()


###############
# HVAC
###############
def add_hvac(location: Location, x: int, y: int, name: str, wattage: int) -> HVAC:
    """

    :param location:
    :param name:
    :param wattage:
    :return:
    """
    newhvac = HVAC(location, x, y, name, wattage)
    commit(newhvac)
    return newhvac


def set_hvac_params(hvacsystem: HVAC, set_f: int, high_f: int, low_f: int, int_f: int, ext_f: int) -> None:
    """

    :param hvacsystem:
    :param set_f The temperature in degrees F to set the house to
    :param high_f: The temperature in degrees to automatically switch to COOL
    :param low_f: The temperature in degrees to automatically switch to HEAT
    :param int_f: The temperature of the house in F
    :param ext_f: The temperature of outside in F
    :return:
    """
    # Ensure high temp is not less than low temp
    assert high_f > low_f
    assert high_f > set_f and set_f > low_f

    hvacsystem.set_f = set_f
    hvacsystem.int_f = int_f
    hvacsystem.ext_f = ext_f
    hvacsystem.high_f = high_f
    hvacsystem.low_f = low_f

    commit(hvacsystem)


def get_hvac_systems() -> List[HVAC]:
    return HVAC.query.all()


def set_hvac_systems(setf, highf, lowf) -> List[HVAC]:
    # Ensure high temp is not less than low temp
    assert highf > lowf
    assert highf > setf and setf > lowf

    HVAC.query.update({HVAC.set_f: setf, HVAC.high_f: highf, HVAC.low_f: lowf})
    db.session.commit()
    return HVAC.query.all()


###############
# Generic Device Queries
###############
def get_devices() -> List[Device]:
    """

    :return:
    """
    return Device.query.order_by(Device.deviceId.asc()).all()


def get_device_by_name(name: str) -> Device:
    """

    :param name:
    :return:
    """
    return Device.query.filter(Light.name.ilike(name)).first()


def get_device_by_id(did: int) -> Device:
    """

    :param did:
    :return:
    """
    return Device.query.filter(Device.deviceId == did).first()


def set_device_state(did: int, state: str) -> bool:
    try:
        Device.query.filter(Device.deviceId == did).update(
            {Device.state: state})
        db.session.commit()
        device = Device.query.filter(Device.deviceId == did).first()
        return device
    except:
        return False
