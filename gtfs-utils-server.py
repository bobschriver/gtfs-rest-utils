#!flask/bin/python
from flask import Flask
from flask.ext.jsonpify import jsonify
import sys, getopt
from GTFSParser import GTFSCSVParser

app = Flask(__name__)

agencies = {
        'agencies': [
            { 
                'agency_id': 1,
                'agency_name': 'Metro Transit'
                },
            {
                'agency_id': 40,
                'agency_name': 'Sound Transit'
                }
            ]
        }

routes = {
        1: {
            'routes': [
                {
                    'route_id': 10001,
                    'route_short_name': '1'
                    }
                ]
            },
        40: {
            'routes': [
                {
                    'route_id': 594,
                    'route_short_name': '594'
                    }
                ]
            }
        }

gtfs_parser = GTFSCSVParser()

@app.route('/api/v1.0/agencies', methods=['GET'])
def get_agencies():
    return jsonify(gtfs_parser.get_agencies())

@app.route('/api/v1.0/routes/<int:agency_id>', methods=['GET'])
def get_routes(agency_id):
    return jsonify(routes[agency_id])

def main(argv):
    opts, args = getopt.getopt(argv, "", ["agency-filename="])

    for opt, arg in opts:
        if opt == "--agency-filename":
            agency_filename = arg
            gtfs_parser.parse_agency_file(arg)

if __name__ == '__main__':
    main(sys.argv[1:])
    app.run(debug=True)
