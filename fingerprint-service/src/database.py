from cassandra.cluster import Cluster
from cassandra.query import dict_factory

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory