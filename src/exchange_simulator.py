"""
Simulates a live exchange by publishing data from a file on disk.

Run on Kafka node.
"""
import json
import os
import time

from json import dumps
from kafka import KafkaProducer

# Load configs
configs = json.load(open('./conf/kafka.json'))


def main():
    data_file = open(configs['data_file'])

    # Create Kafka producer (this will run on the same machine as Kafka)
    pusher = KafkaProducer(bootstrap_servers=configs['kafka_ip'],
                           value_serializer=lambda x: dumps(x).encode('utf-8'))

    while True:
        # Each row represents an API response serving ticks over the last second
        row = loop_file(data_file)

        ticks = json.loads(row)
        # Write simulated real-time timestamp
        for t in ticks:
            t['date'] = time.time()

        # Send prices to Kafka
        pusher.send(topic=configs['kafka_topic'], value=ticks)
        pusher.flush()

        # Print the time so user can tell the program is alive
        t = time.time()
        print(t)

        # Wait 1 second to simulate ~1 hz API call frequency
        time.sleep(1)


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
