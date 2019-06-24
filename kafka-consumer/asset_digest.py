"""
Calculates per-asset summary statistics and writes them to database. Run on Kafka server.
"""
import json

from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine.models import Model
from kafka import KafkaConsumer

from PriceQueue import PriceData

# Folder containing test price data
data_dir = 'test-tiny'
topic = 'price'


class AssetStat(Model):
    asset = columns.Text(primary_key=True)
    time_collected = columns.Float()
    reward = columns.Float()
    risk = columns.Float()


def main():
    # Connect to cassandra
    keyspace = 'silverbullet'
    connection.setup(['10.0.0.5'], keyspace)
    create_keyspace_simple(keyspace, 3)

    # Make sure the table exists
    sync_table(AssetStat, keyspaces=[keyspace])

    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer('price', bootstrap_servers='localhost')

    # Define a window over a certain prices from Kafka
    pd = PriceData(60)

    # Process Kafka messages
    for msg in consumer:
        # Parse message
        s = msg.value
        d = json.loads(s)

        # Process prices
        for asset in d['prices']:
            price = float(d['prices'][asset])
            pd.push_price(asset, price, d['timestamp'])

            # Write to cassandra
            pq = pd.data[asset]
            AssetStat(asset=asset).timeout(1).update(
                reward=pq.reward,
                risk=pq.risk,
                time_collected=pq.price_data[-1].timestamp)


if __name__ == '__main__':
    main()
