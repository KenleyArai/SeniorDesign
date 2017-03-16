import json
from collections import defaultdict
from cassandra.cluster import Cluster

class Point(object):
    # This object should be static
    def __init__(self, lon=0, lat=0, properties=None):
        self.lon = lon
        self.lat = lat
        self.properties = properties or {}

    def get_geojson(self):
        feature = defaultdict(str)
        point = defaultdict(str)

        point["type"] = "Point"
        point["coordinates"] = [self.lon, self.lat]

        feature["type"] = "Feature"
        feature["geometry"] = point
        feature["properties"] = self.properties

        return feature

class CollectionPoints(object):
    def __init__(self):
        self.points = []

    def add(self, point):
        if point:
            self.points.append(point)

    def get_geojson(self):
        collection = defaultdict(str)
        collection['type'] = "FeatureCollection"
        collection['features'] = [feature.get_geojson() for feature in self.points]
        return collection

class Connector(object):

    def __init__(self, port=9043):
        self.port = port
        self.conn = Cluster(port=port)
        self.session = None
        self.lookup_stmts = None
    
    def connect(self):
        if self.session is None:
            self.session = self.conn.connect()
            self.lookup_stmts = { 
                'get hospitals by state': self.session.prepare("SELECT lon, lat FROM hospitals2.info WHERE state=?"),
                'get hospitals': self.session.prepare("SELECT lon, lat FROM hospitals2.info")
            }


    def get_hospital_points(self, state=None):
        collection = CollectionPoints()
        rows = None
        if state:
            rows = self.session.execute(self.lookup_stmts['get hospitals by state'], [state])
        else:
            rows = self.session.execute(self.lookup_stmts['get hospitals'])

        for lon, lat in rows:
            collection.add(Point(lon, lat))

        return collection.get_geojson()