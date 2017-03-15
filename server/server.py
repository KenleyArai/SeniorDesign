from flask import Flask
from flask_restful import Resource, Api
from connector import Connector

app = Flask(__name__)
api = Api(app)

class MapAPI(Resource):
    def get(self):
        connector = Connector()
        return connector.get_providers_count()

api.add_resource(MapAPI, '/')

if __name__ == '__main__':
    app.run()