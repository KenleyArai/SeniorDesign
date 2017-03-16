from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from connector import Connector

app = Flask(__name__)
api = Api(app)

CONN = Connector()
CONN.connect()

class HospitalAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('state')

        args = parser.parse_args()

        if args['state']:
            return jsonify(CONN.get_hospital())
        return jsonify(CONN.get_hospital_points(args['state']))

api.add_resource(HospitalAPI, '/hospitals', endpoint='hospitals')

if __name__ == '__main__':
    app.run(debug=True)