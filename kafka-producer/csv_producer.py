"""
Simulates a live exchange by publishing data from a file on disk.
"""

import os
import time

from json import dumps
from kafka import KafkaProducer

# Folder containing test price data
data_dir = 'test-tiny'
topic = 'price'


def main():
    price_data = open_file_handles(data_dir)

    # Create kafka producer (this will run on the same machine as Kafka)
    pusher = KafkaProducer(bootstrap_servers='localhost',
                           value_serializer=lambda x: dumps(x).encode('utf-8'),
                           key_serializer=lambda x: dumps(x).encode('utf-8'))

    while True:
        # Read 1 price for each asset
        prices = dict(map(lambda asset: (asset, float(loop_file(price_data[asset]))), price_data))
        t = time.time()

        # Temporarily writing with console instead of API because the latter doesn't work.
        write_prices_to_kafka_with_api(prices, pusher, t)

        # Print the time so we can tell the program is alive
        print(t)

        # Wait 1 seconds to simulate ~1 hz price resolution
        time.sleep(1)

    return


def write_prices_to_kafka_with_api(prices, pusher, t):
    """
    Publishes the given prices to Kafka, using the API, and adds the given timestamp.

    The timestamp is provided separately so that it can be added to the message content. Kafka does also timestamp
    messages by itself. However, those are UNIX timestamps (seconds) and don't have enough resolution for our purposes.

    :param prices: Prices, in the form of a dict(asset_name, price)
    :param pusher: Kafka pusher object initialized with the correct serializers (JSON recommended)
    :param t: Timestamp (will be written into the message, Kafka also maintains its own timestamp)
    :return:
    """

    for asset, price in prices.items():
        # Push prices to Kafka TODO: This method can also set a key, but setting it seems to make messages not show up in Kafka.
        pusher.send(topic=topic, value={'asset': asset, 'price': price, 'timestamp': t})

    pusher.flush()


def open_file_handles(folder):
    """
    Opens file handles to price data inside the given folder.

    Each file is expected to be a text file with one price per line, and no blank lines.

    :param folder: Folder with data files
    :return: Map from asset name (filename) to file handle
    """

    all_files = os.listdir(folder)

    handles = {}
    for f in all_files:
        # Infer asset name from extension
        name = os.path.splitext(f)[0]
        handles[name] = open(os.path.join(folder, f))

    return handles


def loop_file(file_handle):
    """
    Reads one line from the given file. If we are at the end of the file, returns to the beginning. Call repeatedly to
    create an infinite loop from the file.

    The file should multiple lines, and none of them should be blank.

    :param file_handle: Handle to file.
    :return: Contents of line the handle was pointing to.
    """

    line = file_handle.readline()

    # We assume empty line means end of file. TODO: Implement better EOF detection.
    if line == '':
        print('End of file, looping over...')
        file_handle.seek(0)
        line = file_handle.readline()

    return line.strip()


if __name__ == '__main__':
    main()
