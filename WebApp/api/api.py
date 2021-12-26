# Laptop Service

from flask import Flask, make_response, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import pymongo
import arrow
import os

import logging

#Credits
# Use for knowing how to send out data as csv
# LInk: https://stackoverflow.com/questions/26997679/writing-a-csv-from-flask-framework

# Instantiate the app
app = Flask(__name__)
api = Api(app)

try:
    mongo_client = os.environ['DB_PORT_27017_TCP_ADDR']
except:
    mongo_client = "db"
client = client = MongoClient(mongo_client, 27017)
db = client.brevetsdb

def _get_brevet_info(open_only=False, close_only=False, top=None):
    """
    Provideds a formatted dictionary of the brevets.
    note: open_only and close_only can not both be true
    args: json creation information
        open_only: bool, if only opens are to be returned
        close_only: bool, if only closed are to be returned
        top: int, the number of lowest opening times to be returned
            if top >= 9999 it is assumed no top was "truely" provided
    returns: dictionary in the following format
        {'id': str,
        'distance': int,
        'begin_date': str format MM/DD/YYYY,
        'begin_time': str format HH:mm,
        'controls': list of all controls
            format
            {'km': int,
            'mi': int,
            'location': str,
            'open': str,
            'close': str}
        }
    """
    assert not(open_only and close_only)
    top_exists = top is not None
    if top_exists:
        top = int(top)
        top_exists = top < 9999

    brevets = []

    _brevets = db.brevetsdb.find()

    if top_exists:
        top = int(top)
        _brevets.sort([
            ('open', pymongo.ASCENDING),
            ])
        _brevets.limit(top)
    else:
        _brevets.sort([
            ('sub_time', pymongo.ASCENDING),
            ('km', pymongo.ASCENDING),
            ])

    for brevet in _brevets:
        app.logger.debug(brevet)
        index = len(brevets)-1
        is_new_brevet = True

        controle_info = {'km': brevet['km'],
                        'mi': brevet['mi'],
                        'location': brevet['location']}

        if not open_only:
            controle_info['close'] = brevet['close']

        if not close_only:
            controle_info['open'] = brevet['open']

        if not top_exists:
            for item in brevets:
                if item['id'] == brevet['sub_time']:
                    item['controls'].append(controle_info)
                    is_new_brevet = False
                    break

        if is_new_brevet:
            arrow_time = arrow.get(brevet['date_time'])
            index += 1
            brevets.append({'controls':[]})
            brevets[index]['id'] = brevet['sub_time']
            brevets[index]['distance'] = brevet['distance']
            brevets[index]['begin_date'] = arrow_time.format('MM/DD/YYYY')
            brevets[index]['begin_time'] = arrow_time.format('HH:mm')
            brevets[index]['controls'].append(controle_info)

    return {"brevets": brevets}


def _create_csv(open_only=False, close_only=False, top=None):
    """
    args: json creation information required
        open_only: bool, if only opens are to be returned
        close_only: bool, if only closed are to be returned
        top: int, the number of lowest opening times to be returned
    returns: csv format of the json file
    """

    brevets =  _get_brevet_info(open_only=open_only, close_only=close_only, top=top)

    csv_data = "brevets/distance,brevets/begin_date,brevets/begin_time,brevets/controls/0/km,brevets/controls/0/mi,brevets/controls/0/location"

    if not close_only:
        csv_data += ",brevets/controls/0/open"

    if not open_only:
        csv_data += ",brevets/controls/0/close"

    csv_data += "\n"
    for brvt in brevets['brevets']:
        for control in brvt['controls']:
            csv_data += str(brvt['distance']) + ","
            csv_data += brvt['begin_date'] + ","
            csv_data += brvt['begin_time'] + ","
            csv_data += str(control['km']) + ","
            csv_data += str(control['mi']) + ","
            csv_data += control['location']
            if not close_only:
                csv_data += "," + control['open']

            if not open_only:
                csv_data += "," + control['close']
            csv_data += "\n"

    output = make_response(csv_data)
    output.headers["Content-Type"] = "text/csv"
    return output

class ListAll(Resource):
    def get(self):
        top = request.args.get("top", None)
        all_points = _get_brevet_info(top=top)
        return all_points

class OpenOnly(Resource):
    def get(self):
        top = request.args.get("top", None)
        open_only = _get_brevet_info(open_only=True, top=top)
        return open_only

class CloseOnly(Resource):
    def get(self):
        top = request.args.get("top", None)
        open_only = _get_brevet_info(close_only=True, top=top)
        return open_only

class AllCSV(Resource):
    def get(self):
        top = request.args.get("top", None)
        return _create_csv(top=top)

class OpenCSV(Resource):
    def get(self):
        top = request.args.get("top", None)
        return _create_csv(open_only=True, top=top)

class CloseCSV(Resource):
    def get(self):
        top = request.args.get("top", None)
        return _create_csv(close_only=True, top=top)

# Create routes
# Another way, without decorators
api.add_resource(ListAll, '/listAll', '/listAll/json')
api.add_resource(OpenOnly, '/listOpenOnly', '/listOpenOnly/json')
api.add_resource(CloseOnly, '/listCloseOnly', '/listCloseOnly/json')
api.add_resource(AllCSV, '/listAll/csv')
api.add_resource(OpenCSV, '/listOpenOnly/csv')
api.add_resource(CloseCSV, '/listCloseOnly/csv')

# Run the application
if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=80, debug=True)
