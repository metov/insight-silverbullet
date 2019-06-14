To install Kafka:

* Set up [Pegasus](https://github.com/InsightDataScience/pegasus)
* We need to create EC2 nodes for Kafka: `peg up kafka-cluster.yml`
	* You can create this from `kafka-cluster-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Fetch with `peg fetch kafka-cluster` (`peg install` won't run without it)
* Install `bc` (zookeeper won't install properly without it): `peg sshcmd-cluster kafka-cluster "sudo apt install -y bc"`
* Install Kafka: ` peg install kafka-cluster kafka`

This will create 3 nodes running Kafka with Zookeeper. In production, it would be better to have dedicated nodes for Zookeeper, but in this case the same nodes run both.
