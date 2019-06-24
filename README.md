# SilverBullet
Take your best shot at crypto markets!

SilverBullet live optimization of cryptocurrency portfolio with very low latency, suited to high-frequency trading applications.

## Problem statement
Split second decisions can mean the difference between profit and ruin in modern markets. To fully exploit the economic potential of the market, a trading system must be able to evaluate market conditions with extremely high latency. If this takes too long, by the time trading decisions are made, the situation will have changed. I want to create an architecture that enables such low latency, live analysis of financial price data.

## General solution
I will use state of the art, blazing fast stream processing framework Flink to take in a live ticker data from an exchange, and distribute financial computation to a computing cluster. The system will be designed for minimal latency; as a second concern, I will construct a scalable computing cluster that can handle heavy computations. As a demonstration, I will implement a Monte Carlo approach to finding most efficient portfolios according to modern portfolio theory. The results will be shown live in a Web UI, as well as served through an API for high frequency trading software.

## Setup

* Set up Kafka as described in [kafka-setup](setup/kafka/kafka-setup.md)
	* Kafka is a distributed, fault tolerant message queue. Kafka will ingest the price data into a message queue and make it available to other programs.
* Set up Spark as described in [spark-setup](setup/spark/spark-setup.md)
	* Apache Spark is a distributed processing framework. Spark will do the distributed computations.
* Set up Cassandra as described in [cassandra-setup](setup/cassandra/cassandra-setup.md)
	* Cassandra is a distributed database. It will store computation results.

### Sending messages to Kafka
In order to write to Kafka, you need a Kafka producer. There is a "console producer" that lets you manually push messages by typing to console. To write programmatically, you need to write a [Kafka producer program](kafka-producer/kafka-producer.md).
