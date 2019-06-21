import json

from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def main():
    """
    Applies ETL on Spark stream

    Run with /usr/local/spark/bin/spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.3.1.jar kafka_stdev.py
    Activate producer and wait for a while

    :return:
    """

    kafka_port = '9092'
    kafka_ips = ['10.0.0.4', '10.0.0.8', '10.0.0.11']
    kafka_urls = ','.join(['{}:{}'.format(s, kafka_port) for s in kafka_ips])

    # Dunno what this is but you have to provide
    batch_duration = 1

    # Initialize session
    spark_session = SparkSession \
        .builder \
        .appName("asset-average") \
        .getOrCreate()

    spark_context = spark_session.sparkContext

    # Create streaming context (=connection to Spark
    streaming_context = StreamingContext(spark_context, batch_duration)

    # Read from Kafka
    input = KafkaUtils \
        .createDirectStream(streaming_context, ['price'], {"metadata.broker.list": kafka_urls})

    # Transform
    jsons = input.window(5000).map(lambda t: t[1]).map(json.loads)

    prices = jsons.map(lambda d: d['price'])

    total = prices.reduce(lambda x, y: x+y)

    total.pprint()

    # Execute calculations
    streaming_context.start()
    streaming_context.awaitTermination()


if __name__ == "__main__":
    main()
