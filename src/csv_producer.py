"""
Simulates a live exchange by publishing data from a file on disk.
"""
import json
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
                           value_serializer=lambda x: dumps(x).encode('utf-8'))

    while True:
        # Read 1 price for each asset
        datum = read_prices(price_data)
        t = time.time()

        # Send prices to Kafka
        pusher.send(topic=topic, value=datum)
        pusher.flush()

        # Print the time so we can tell the program is alive
        print(t)

        # Wait 1 seconds to simulate ~1 hz price resolution
        time.sleep(1)


def read_prices(price_data):
    datum = {
        'prices': {},
        'timestamp': (time.time())
    }

    for asset, f in price_data.items():
        datum['prices'][asset] = loop_file(f)

    return datum


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
