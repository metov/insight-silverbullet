## Getting the files on Kafka cluster
Pegasus can send files with SCP: 
* Mock producer: `peg scp to-rem kafka-cluster 1 csv_producer.py csv_producer.py`
* Test data: `peg scp to-rem kafka-cluster peg scp to-rem kafka-cluster 1 test-tiny test-tiny`

## Creating topic
Before we can publish to Kafka, the topics must be created. Kafka can also [auto-create topics](https://help.aiven.io/articles/1816851-kafka-topic-auto-create), but that feature is not used here.

SSH into Kafka: `peg ssh kafka-cluster 1`

Then run the following command:
``` bash
/usr/local/kafka/bin/kafka-topics.sh \
	--create --zookeeper localhost:2181 \
	--replication-factor 3 \
	--partitions 10 \
	--topic price
```

Note the Kafka path, replication factor, partition number and topic name.

## Running the producer
You will probably need to install the library on the node you're SSHing into: `pip install kafka`

You can run the producer with `python csv_producer.py`. Stop with Ctrl+C. To see messages run `/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic price --from-beginning`.

