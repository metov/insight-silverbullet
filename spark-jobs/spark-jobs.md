# Spark jobs
A very simple template for a Kafka-PySpark job is in `kafka_copy.py`. Run with `/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1 kafka_copy.py`. The package argument is necessary to satisfy Kafka connector dependency.

After running `kafka_copy.py`, write some messages in topic `price` on Kafka. They will be copied to topic `result`.

## Interactive shell
Run `/usr/local/spark/bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1` for interactive PySpark shell with Kafka support.

## Logs
Spark likes to spam the console when you submit jobs. To reduce this, we need to set a value in the log4j configs.

```
cp /usr/local/spark/conf/log4j.properties.template /usr/local/spark/conf/log4j.properties
nano /usr/local/spark/conf/log4j.properties
```

And set `log4j.rootCategory` to `ERROR`.
