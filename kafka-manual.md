# Manual Kafka Administration
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

Note the Kafka path, replication factor, partition number and topic name. You can see the existing topics with: `/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181`

### Manual testing
All commands here call the scripts that come with Kafka and have a "localhost" argument - so you have to run them from a shell on your Kafka node, and it is assumed that there's a Zookeper running on the same node. If you followed the [Kafka setup instructions](setup/kafka/kafka-setup.md), you can do `peg ssh kafka-cluster 1` and type these commands there.

#### Topic management
 
##### Create a test topic
``` bash
/usr/local/kafka/bin/kafka-topics.sh \
	--create --zookeeper localhost:2181 \
	--replication-factor 1 \
	--partitions 1 \
	--topic test
```

(based on [official docs](https://kafka.apache.org/quickstart#quickstart_createtopic))

##### List all topics
To list topics: `/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181`

#### Write messages from console
Interactive console producer: `/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test`

Just write as a single command: `echo "my test message" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test`

#### Read messages from console
To read messages: `/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning`

#### Delete topics
To delete topic: `/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic test`

You will get a warning about `delete.topic.enable` needing to be set. This is fine, it seems to be set by the pegasus install script (if in doubt, check by listing topics after deleting).


