Before we can publish to Kafka, the topics must be created. Kafka can also [auto-create topics](https://help.aiven.io/articles/1816851-kafka-topic-auto-create), but that feature is not used here. Run the following command:
``` bash
/usr/local/kafka/bin/kafka-topics.sh \
	--create --zookeeper localhost:2181 \
	--replication-factor 3 \
	--partitions 10 \
	--topic price
```

Note the kafka path, replication factor, partition number and topic name.
