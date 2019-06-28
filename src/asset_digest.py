"""
Calculates per-asset summary statistics and writes them to database. Run on Kafka server.
"""
import time
import uuid

from cassandra.cqlengine.management import sync_table
from kafka import KafkaConsumer
from PriceQueue import PriceData
from cassandra_models import AssetStat, AssetLatencyLog
from cassandra_utilities import *

# Load configs
configs = json.load(open('./conf/kafka.json'))


def main():
    connect_to_cassandra()
    initialize_keyspace(silverbullet_keyspace)

    # Make sure the table exists
    sync_table(AssetStat, keyspaces=[silverbullet_keyspace])
    sync_table(AssetLatencyLog, keyspaces=[silverbullet_keyspace])

    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(configs['kafka_topic'], bootstrap_servers=configs['kafka_ip'])

    # Define a window over certain prices from Kafka
    pd = PriceData(configs['window_size'])

    # Process Kafka messages
    for msg in consumer:
        # Parse message
        s = msg.value
        ticks = json.loads(s)

        latencies = []

        # Process prices
        for tick in ticks:
            price = tick['price']
            asset = tick['asset']
            timestamp = tick['date']

            # Check for division by zero errors caused by insufficient time resolution
            if pd.will_divide_by_zero(asset, timestamp):
                print('Two ticks happened in the same millisecond - {} - ignoring the later one.'.format(timestamp))
                continue

            # Process this tick and update reward/risk
            pd.push_price(asset, price, timestamp)

            # Write to cassandra
            pq = pd.data[asset]
            t = time.time()
            dt = t - pq.price_data[-1].timestamp
            AssetStat(asset=asset).timeout(1).update(reward=pq.reward, risk=pq.risk, time_evaluated=t, latency=dt)

            latencies += [dt]

        # Record latencies for this message
        t = time.time()
        AssetLatencyLog.create(id=uuid.uuid1(),
                               time_evaluated=int(t),
                               latency_mean=sum(latencies) / len(latencies),
                               latency_min=min(latencies),
                               latency_max=max(latencies))

        # Print the time so user can tell the program is alive
        print(t)


if __name__ == '__main__':
    main()
