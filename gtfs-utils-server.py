#!flask/bin/python
from flask import Flask,request
from flask.ext.jsonpify import jsonify
import sys, getopt
from GTFSParser import GTFSCSVParser

app = Flask(__name__)

gtfs_parser = GTFSCSVParser()

@app.route('/api/v1.0/agencies', methods=['GET'])
def get_agencies():
    return jsonify(gtfs_parser.get_agencies())

@app.route('/api/v1.0/agency_id', methods=['GET'])
def agency_id_by_name():
    agency_name = request.args.get('agency_name')
    return jsonify(gtfs_parser.get_agency_id_by_name(agency_name))

@app.route('/api/v1.0/route_id', methods=['GET'])
def route_id_by_name():
    route_name = request.args.get('route_name')
    print(route_name)
    agency_id = request.args.get('agency_id')
    print(agency_id)
    return jsonify(gtfs_parser.get_route_id_by_name(agency_id, route_name))

@app.route('/api/v1.0/stop_ids', methods=['GET'])
def stop_ids_by_name():
    stop_name = request.args.get('stop_name')
    print(stop_name)
    return jsonify(gtfs_parser.get_stop_ids_by_name(stop_name))

@app.route('/api/v1.0/first_trip_between_stops', methods=['GET'])
def first_trip_between_stops():
    first_stop_id = request.args.get('first_stop_id')
    last_stop_id = request.args.get('last_stop_id')
    route_id = request.args.get('route_id')
    
    return jsonify(gtfs_parser.get_first_trip_between_stops(first_stop_id, last_stop_id, route_id))

@app.route('/api/v1.0/shape_between_stops', methods=['GET'])
def shape_between_stops():
    first_stop_id = request.args.get('first_stop_id')
    last_stop_id = request.args.get('last_stop_id')
    trip_id = request.args.get('trip_id')

    return jsonify(gtfs_parser.get_shape_between_stops_by_trip(first_stop_id, last_stop_id, trip_id))

def main(argv):
    opts, args = getopt.getopt(argv, "", ["agency-filename=", "routes-filename=", "stops-filename=", "trips-filename=", "stop_times-filename=", "shapes-filename="])

    for opt, arg in opts:
        if opt == "--agency-filename":
            agency_filename = arg
        elif opt == "--routes-filename":
            routes_filename = arg
        elif opt == "--stops-filename":
            stops_filename = arg
        elif opt == "--trips-filename":
            trips_filename = arg
        elif opt == "--stop_times-filename":
            stop_times_filename = arg
        elif opt == "--shapes-filename":
            shapes_filename = arg

    gtfs_parser.parse_agency_file(agency_filename)
    print('Loaded agency file')
    gtfs_parser.parse_routes_file(routes_filename)
    print('Loaded routes file')
    gtfs_parser.parse_stops_file(stops_filename)
    print('Loaded stops file')
    gtfs_parser.parse_trips_file(trips_filename)
    print('Loaded trips file')
    gtfs_parser.parse_trip_shape(trips_filename, stops_filename, stop_times_filename, shapes_filename)
    print('Loaded trip shape')

if __name__ == '__main__':
    main(sys.argv[1:])
    app.run(debug=True)
