"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config, os
from pymongo import MongoClient
import pymongo

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

try:
    mongo_client = os.environ['DB_PORT_27017_TCP_ADDR']
except:
    mongo_client = "db"
client = client = MongoClient(mongo_client, 27017)
db = client.brevetsdb

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.errorhandler(400)
def input_error(error):
    app.logger.debug("Input error")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('400.html'), 400

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    date_time = request.args.get('date_time', type=str)
    date_time = arrow.get(date_time).isoformat()

    brevet_dist = request.args.get('dist', type=int)

    open_time = acp_times.open_time(km, brevet_dist, date_time)
    close_time = acp_times.close_time(km, brevet_dist, date_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_submit")
def _submit():
    """
    Submits the entries to the database
    """
    submission = request.args.get('submission_time', type=str)
    distance = request.args.get('distance', type=int)
    date_time = request.args.get('date_time', type=str)
    km = request.args.get('km', type=float)
    mi = request.args.get('mi', type=float)
    location = request.args.get('location', type=str)
    open_time = request.args.get('open', type=str)
    close_time = request.args.get('close', type=str)

    arrow_time = arrow.get(date_time)
    begin_date = arrow_time.format('MM/DD/YYYY')
    begint_time = arrow_time.format('HH:mm')

    item_doc = {
        'sub_time': submission,
        'distance': distance,
        'date_time': date_time,
        'km': km,
        'mi': mi,
        'location': location,
        'open': open_time,
        'close': close_time
        }
    db.brevetsdb.insert_one(item_doc)

    result = {"msg": "Test Message"}
    return flask.jsonify(result=result)

@app.route("/_display", methods=['GET'])
def _display():
    """
    Renders the brevet times in the database
    """
    brevets = []

    _brevets = db.brevetsdb.find()

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
                        'location': brevet['location'],
                        'close': brevet['close'],
                        'open': brevet['open']}

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

    info = {'total_brevets': len(brevets)}
    return flask.render_template('display.html', brevets=brevets, info=info)

@app.route("/_test", methods=['GET'])
def _test():
    return flask.render_template('index.php')

@app.route("/_error", methods=['GET'])
def _error():
    """
    Renders an error in input
    """
    return flask.render_template('400.html'), 400

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(host="0.0.0.0")
