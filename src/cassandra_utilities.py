"""
Contains utility methods for accessing Cassandra.
"""

import json

from cassandra.cqlengine import connection

# Load configs
from cassandra.cqlengine.management import create_keyspace_simple

cassandra_configs = json.load(open('./conf/cassandra.json'))
silverbullet_keyspace = cassandra_configs['keyspace']


def connect_to_cassandra():
    connection.setup(cassandra_configs['ips'], silverbullet_keyspace)


def initialize_keyspace(keyspace):
    create_keyspace_simple(keyspace, 3)