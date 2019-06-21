# Kafka setup
## Installing Kafka:

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
	* There's a bug where sometimes a daily apt update service will linger for a while, locking `/var/lib/dpkg/lock` and preventing you from installing anything. You can check if anything is locking this with `peg sshcmd-cluster kafka-cluster "sudo fuser /var/lib/dpkg/lock"`. Manually unlocking it or terminating the apt process is dangerous as it can corrupt the packages - the safest option is to simply wait. Usually after about 20 minutes the lock will be released.
* Install SSH: `peg install kafka-cluster ssh`
* Install AWS credentials: `peg install kafka-cluster aws`
* Zookeeper is required for Kafka: `peg install kafka-cluster zookeeper`
* Install Kafka: `peg install kafka-cluster kafka`
* Start Zookeeper: `peg service kafka-cluster zookeeper start` (must start before kafka)
* Start Kafka: `peg service kafka-cluster kafka start` (if console gets stuck, Ctrl+C is safe)

This will create 3 nodes running Kafka with Zookeeper. In production, it would be better to have dedicated nodes for Zookeeper, but in this case the same nodes run both.

## Stopping when not in use
When you're not using the cluster, you can stop it temporarily to avoid being billed.

* Stop Kafka: `peg service kafka-cluster kafka stop`
* Stop Zookeeper: `peg service kafka-cluster zookeeper stop`
* Stop cluster: `peg stop kafka-cluster` (answer y)

### Resuming
You have to start the services in the correct order:

* Start cluster: `peg start kafka-cluster`
* Start Zookeeper: `peg service kafka-cluster zookeeper start`
* Start Kafka: `peg service kafka-cluster kafka start`

**Please note:** With the current config, message data is stored in `/tmp`, which is wiped on shutdown by Linux. However, it seems that topic definitions will not be wiped. As a result, on resume Kafka will still have the same topics, but their contents will be lost. However the offset will still point to the lost messaged, and as a result Kafka consumers may report data loss has occurred (which is technically true). For this project, this is inconsequent beyond requiring an extra command to ignore the data loss.
