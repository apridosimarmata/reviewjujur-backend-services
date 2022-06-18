from cassandra.cluster import Cluster
from cassandra.query import dict_factory

cluster = Cluster(['172.17.0.2'])
session = cluster.connect('review')
session.row_factory = dict_factory
