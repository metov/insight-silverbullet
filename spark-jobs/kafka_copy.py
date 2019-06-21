from pyspark.sql import SparkSession


def main():
    """
    Copies messages from one Kafka topic ('price') to another ('result'). Will only handle messages sent to Kafka
    after this script has started running.

    :return:
    """

    kafka_port = '9092'
    kafka_ips = ['10.0.0.4', '10.0.0.8', '10.0.0.11']
    kafka_urls = ','.join(['{}:{}'.format(s, kafka_port) for s in kafka_ips])

    # Initialize session
    spark_session = SparkSession \
        .builder \
        .appName("StructuredNetworkWordCount") \
        .getOrCreate()

    # Read from Kafka
    df = spark_session \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_urls) \
        .option("subscribe", "price") \
        .option('failOnDataLoss', 'false') \
        .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Write to Kafka TODO: Checkpoint location - not sure what this location does, need to understand how checkpoints work.
    ds = df \
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_urls) \
        .option("topic", "result") \
        .option('checkpointLocation', 'checkpoint') \
        .start()

    ds.awaitTermination()


if __name__ == "__main__":
    main()
