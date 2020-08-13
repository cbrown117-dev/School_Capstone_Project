from flask import Blueprint, url_for, request
from flask_restplus import Api

# Define API blueprints and API spec for flask
apiv1 = Blueprint('api', __name__)
api = Api(apiv1, version='1.0', title='HomeIOT API',
          description='The HomeIOT Application REST API for CS499 Team 5')

# Define namespaces
locations_ns = api.namespace('location', 'Location methods')
devices_ns = api.namespace('device', 'Device methods')
usage_ns = api.namespace('usage', 'Device usage information')

# Fix of returning swagger.json on HTTP
@property
def specs_url(self):
    """
    The Swagger specifications absolute url (ie. `swagger.json`)

    :rtype: str
    """
    return url_for(self.endpoint('specs'), _external=False)

Api.specs_url = specs_url
