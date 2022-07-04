from cassandra.cluster import Cluster
from cassandra.query import dict_factory

cluster = Cluster(['172.17.0.2'])
session = cluster.connect('review')
session.row_factory = dict_factory

statuses_key = {}

statuses = session.execute('SELECT * FROM status')

query = 'SELECT * FROM business_reviews'
sum = 0
count = 0
for row in session.execute(query):
    if row.get('business_uid') == '12283f02-a4ff-4516-9ab3-657a8f7580eb' and len(row.get('phone_uid')) > 1:
        print(row)
        sum += row.get('score')
        count += 1

print(sum)
print(count)
