from cassandra.cluster import Cluster
import json

class Connector(object):
    
    def __init__(self, port=9043):
        self.port = port
        self.conn = Cluster(port=port)
        self.session = None
    
    def connect(self):
        if self.session is None:
            self.session = self.conn.connect()

    def get_providers_count(self, state='CA'):
        with open('./mock.json') as data_file:
            return json.load(data_file)

    # Todo: create query methods