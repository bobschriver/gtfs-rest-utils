#!flask/bin/python
from flask import Flask, jsonify

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

@app.route('/api/v1.0/agencies', methods=['GET'])
def get_agencies():
    return jsonify(agencies)

@app.route('/api/v1.0/routes/<int:agency_id>', methods=['GET'])
def get_routes(agency_id):
    return jsonify(routes[agency_id])

if __name__ == '__main__':
    app.run(debug=True)
