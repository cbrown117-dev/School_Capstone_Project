# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from flask_restplus import Resource, fields
from views.api import api, locations_ns
from dao.location import get_locations
from views.devices import device_model

loc_schema = {
    'locationId': fields.Integer(readonly=True, description='The unique location id'),
    'name': fields.String(required=True, description='The unique location name'),
    'devices': fields.List(fields.Nested(device_model))
}

loc_model = api.model('Location', loc_schema)

@locations_ns.route('')
class Location(Resource):
    '''Gets a list of all available locations'''

    @api.doc(description='Get a list of locations')
    @api.marshal_with(loc_model)
    def get(self):
        '''List all locations'''
        return get_locations()
