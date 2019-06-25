"""
Contains utility methods for accessing Cassandra.
"""

import json

from cassandra.cqlengine import connection

# Load configs
cassandra_configs = json.load(open('./conf/cassandra.json'))


def connect_to_cassandra():
    connection.setup(cassandra_configs['ips'], cassandra_configs['keyspace'])
