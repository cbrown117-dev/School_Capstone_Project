# Contributor(s): Adrian Gose
# If you worked on this file, add your name above so we can keep track of contributions

from datetime import datetime
from flask_restplus import Resource, fields, reqparse
from views.api import api, usage_ns
from dao.usage import *
from dao.events import get_last_10_events_formatted

from werkzeug.exceptions import BadRequest

from generate_functions import Generator

usage_individual = api.model('UsageData', {
    'did': fields.String(required=True, description='The deviceId associated with the UsageData'),
    'd': fields.String(required=True, description='The datetime of the usage aggregation'),
    'v': fields.String(required=True, description='The value of usage, kWh/gallons based on which category context')
})

user_list_fields = api.model('UsageList', {
    'usage': fields.List(fields.Nested(usage_individual)),
})

usage_schema = {
    'usage_date_meta': fields.Nested(api.model('UsageDateMeta', {
        'oldest': fields.String(readonly=True, description='The oldest date available for usage data, in ISO format'),
        'latest': fields.String(readonly=True, description='The latest date available for usage data, in ISO format')
     })),
    'electric': fields.Nested(user_list_fields),
    'water': fields.Nested(user_list_fields)
}

usage_model = api.model('UsageResponse', usage_schema)

@usage_ns.route('/event_history')
class UsageEventLog(Resource):
    """Get an event history for the last 10 events"""

    @api.doc(description='Get an event history for the last 10 events')
    def get(self):
        '''Get an event history for the last 10 events'''

        return get_last_10_events_formatted()

@usage_ns.route('/generate_next')
class UsageGenerateNext(Resource):
    """Generate the next day of data"""

    @api.doc(description='Generate the next day of data')
    def get(self):
        '''Generate the next day of data'''
        print("Generating data api called")
        geninstance = Generator.getInstance()
        geninstance.instantiateSingleton()
        geninstance.generate_next_day_auto()

        return {
            'generated': True
        }

@usage_ns.route('/daterange')
class UsageDateRange(Resource):
    """Get usage date range"""

    @api.doc(description='Get usage date range')
    def get(self):
        '''Get usage date range'''
        return get_usage_month_range()

@usage_ns.route('/usagestats')
@api.doc(params={
    'start': 'Start date in ISO format (YYYY-MM-DD)'
})
class UsageStats(Resource):
    """Get usage statistics for a date range"""

    @api.doc(description='Get usage statistics for a date range')
    def get(self):
        '''Get usage statistics for a date range'''
        parser = reqparse.RequestParser()
        parser.add_argument('start')
        args = parser.parse_args()

        start = validateDate(args['start'])

        if start is None:
            # Default to current month
            end = datetime.datetime.today()
            start = datetime.datetime(end.year, end.month, 1).strftime('%Y-%m-%d')

            print("DATETIME IS ", start)


            
            stats = get_statistics(start)
            graphing = get_graphing_data(start)
            temperatures = get_temperature_data(start)

            return {
                'range': get_usage_month_range(),
                'start': start,
                'stats': stats,
                'temphistory': temperatures,
                'graphing': graphing
            }
        elif start:
            # Use date range specifications

            stats = get_statistics(start)
            graphing = get_graphing_data(start)
            temperatures = get_temperature_data(start)

            return {
                'range': get_usage_month_range(),
                'start': start,
                'stats': stats,
                'temphistory': temperatures,
                'graphing': graphing
            }

@usage_ns.route('/<int:deviceid>')
@usage_ns.param('deviceid', 'The deviceid to get')
@api.doc(params={
    'start': 'Start date in ISO format (YYYY-MM-DD)',
    'end': 'End date in ISO format (YYYY-MM-DD)'
})
class Usage(Resource):
    """Get total usage for a specific deviceid from a specified date range"""

    @api.doc(description='Get total usage for a specific deviceid from a specified date range')
    def get(self, deviceid):
        '''Get total usage for a specific deviceid from a specified date range'''
        parser = reqparse.RequestParser()
        parser.add_argument('start')
        parser.add_argument('end')
        args = parser.parse_args()

        start = validateDate(args['start'])
        end = validateDate(args['end'])

        return {
            'usage_total': get_device_total_usage(deviceid, start, end)
        }

# TODO: Add aggregation type ex. hourly/daily/weekly
@usage_ns.route('')
@api.doc(params={
    'start': 'Start date in ISO format (YYYY-MM-DD)',
    'end': 'End date in ISO format (YYYY-MM-DD)'
})
class UsageList(Resource):
    """Get usage information"""

    @api.doc(description='Get overall usage for the home. If no start/end params are given, this will automatically'
                         'default to the latest day.')
    @api.doc(responses={500: 'Invalid params'})
    @api.marshal_with(usage_model)
    def get(self):
        '''Get usage for a specified date range, in ISO format (YYYY-MM-DD)'''
        parser = reqparse.RequestParser()
        parser.add_argument('start')
        parser.add_argument('end')
        args = parser.parse_args()

        start = validateDate(args['start'])
        end = validateDate(args['end'])

        electric = get_usages(start, end, 'electric', True),
        water  = get_usages(start, end, 'water', True),

        emap = []
        wmap = []

        for el in electric:
            for e in el:
                emap.append({
                    'did': e.deviceId,
                    'd': e.date,
                    'v': e.data
                })

        for el in water:
            for w in el:
                wmap.append({
                    'did': e.deviceId,
                    'd': w.date,
                    'v': w.data
                })

        print(list(emap))

        if start and end:
            return {
                'usage_date_meta': {
                    'oldest': 'todo',
                    'latest': 'todo'
                },
                'electric': {
                    'usage': emap
                },
                'water': {
                    'usage': wmap
                }
            }
        elif not start and not end:
            return {
                'usage_date_meta': {
                    'oldest': 'todo',
                    'latest': 'todo'
                },
                'electric': {
                    'usage': emap
                },
                'water': {
                    'usage': wmap
                }
            }
        else:
            raise BadRequest("Must specify both start and end params")


# Utility functions
def validateDate(date):
    if date is None:
        return None

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        raise BadRequest(f'Date {date} is not valid format YYYY-MM-DD')



