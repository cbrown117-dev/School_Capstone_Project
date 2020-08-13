# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from flask_restplus import Resource, fields, reqparse
from views.api import api, devices_ns
from models.device import Electric, Water
from dao.device import get_devices, set_device_state, get_device_by_id, get_hvac_systems, set_hvac_systems
from generate_functions import Generator
from werkzeug.exceptions import BadRequest

from datetime import datetime, timedelta
import dateutil.parser


device_model = api.model('Device', {
    'deviceId': fields.Integer(readonly=True, description='The unique location id'),
    'name': fields.String(required=True, description='The unique device name'),
    'type': fields.String(required=True, description='The device type'),
    'state': fields.String(enum=['OFF', 'ON', 'OFFLINE', 'ERROR'],
                           default='OFF',
                           required=True,
                           description='The device state'),
    'wattage': fields.Integer(required=False),
    'gpm': fields.Integer(required=False, description='Gallons per minute if device is water type'),
    'set_f': fields.Integer(required=False, description='Temp setpoint of hvac'),
    'high_f': fields.Integer(required=False, description='High triggerpoint of hvac'),
    'low_f': fields.Integer(required=False, description='Low triggerpoint of hvac'),
    'ext_f': fields.Integer(required=False, description='External temperature of home'),
    'int_f': fields.Integer(required=False, description='Internal temperature of home'),
    'x': fields.Integer(required=False, description='X Coordinate for GUI'),
    'y': fields.Integer(required=False, description='Y Coordinate for GUI')
})


@devices_ns.route('')
class Device(Resource):
    '''Gets a list of all available devices'''

    @api.doc(description='Get a list of devices')
    @api.marshal_with(device_model)
    def get(self):
        '''List all devices'''
        return get_devices()


@devices_ns.route('/thermostat')
class HVAC(Resource):
    '''Operations for HVAC systems'''

    @api.doc(description='Get current HVAC settings')
    @api.marshal_with(device_model)
    def get(self):
        '''Get current HVAC settings'''
        return get_hvac_systems()


@devices_ns.route('/thermostat/<int:setf>/<int:highf>/<int:lowf>')
@devices_ns.param('setf', 'The temperature setpoint')
@devices_ns.param('highf', 'The temperature to trigger cooling system')
@devices_ns.param('lowf', 'The temperature to trigger heating system')
class SetHVAC(Resource):
    '''Operations to set HVAC params'''

    @api.doc(description='Set current HVAC settings')
    @api.marshal_with(device_model)
    def put(self, setf, highf, lowf):
        '''Set current HVAC settings'''
        print(setf, highf, lowf)
        try:
            return set_hvac_systems(setf, highf, lowf)
        except AssertionError as e:
            print(e)
            return get_hvac_systems()


@devices_ns.route('/<int:deviceid>')
@devices_ns.param('deviceid', 'The deviceid to get')
class SingleDevice(Resource):
    '''Gets a list of all available devices'''

    @api.doc(description='Get a device by id')
    @api.marshal_with(device_model)
    def get(self, deviceid):
        '''Get a device by id'''
        return get_device_by_id(deviceid)


@devices_ns.route('/<int:deviceid>/setstate/<string:state>')
@devices_ns.param('state', 'The state to set the device. ON, OFF')
@devices_ns.param('deviceid', 'The deviceid to mutate')
@api.doc(params={
    'end': 'End datetime in ISO format'
})
class DeviceMutation(Resource):
    '''Mutations for a specific device'''

    @api.doc(description='Set a specified deviceid state to ON/OFF')
    def put(self, deviceid, state):
        '''Set a device state to ON/OFF'''
        if state is not None and deviceid is not None:
            stateupper = state.upper()
            if stateupper == "ON" or stateupper == "OFF":
                # TODO: DB Manipulate state
                device = set_device_state(deviceid, state)

                geninfo = None

                # Logic to handle device state generation
                if(stateupper == "ON"):
                    # Check if device is electric type
                    if issubclass(type(device), Electric):
                        print("Device is being set to ON and is electric")
                        parser = reqparse.RequestParser()
                        parser.add_argument('end')
                        args = parser.parse_args()

                        end = args['end']

                        # Only process usage if end date is given
                        if end is not None:
                            end = dateutil.parser.parse(end)

                            start_time = datetime.now()
                            end_time = end.replace(tzinfo=None)
                            print(start_time)
                            print(end_time)
                            geninstance = Generator.getInstance()
                            geninfo = geninstance.on_demand_electric_usage(
                                device, start_time, end_time)

                return {
                    'state': state,
                    'deviceid': deviceid,
                    'geninfo': geninfo
                }
            else:
                raise BadRequest("Invalid state. Must be ON/OFF")
        else:
            raise BadRequest(
                "Invalid state. Must specify state and/or deviceid /did/setstate/ON")
