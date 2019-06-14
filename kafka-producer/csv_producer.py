"""
Simulates a live exchange by publishing data from a file on disk.
"""

from kafka import KafkaProducer
from json import dumps

import time
import os

# Folder containing test price data
data_dir = 'test-tiny'


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
        file_handle.seek(0)
        line = file_handle.readline()

    return line.strip()


def main():
    price_data = open_file_handles(data_dir)

    # Create kafka producer (this will run on the same machine as Kafka)
    pusher = KafkaProducer(bootstrap_servers='localhost',
                           value_serializer=lambda x: dumps(x).encode('utf-8'))

    while True:
        # Read 1 price for each asset
        prices = dict(map(lambda asset: (asset, float(loop_file(price_data[asset]))), price_data))
        t = time.time()

        for asset, price in prices.items():
            # Push prices to Kafka
            pusher.send(topic='price',
                        value={'price': price, 'timestamp': t},
                        key={'asset'})

        # Wait 1 second to simulate ~1 hz price resolution
        time.sleep(1)

    return


if __name__ == '__main__':
    main()
