# Cassandra setup
* Set up [Pegasus](https://github.com/InsightDataScience/pegasus)
* Create master node: `peg up cassandra-master.yml`
	* You can create this from `cassandra-master-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Create worker nodes: `peg up cassandra-workers.yml`
	* You can create this from `cassandra-workers-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Fetch with `peg fetch cassandra-cluster`
* Install SSH: `peg install cassandra-cluster ssh`
* Install AWS credentials: `peg install cassandra-cluster aws`
* Finally Cassandra: `peg install cassandra-cluster cassandra`
* Now start Cassandra: `peg service cassandra-cluster cassandra start`  (if console gets stuck, Ctrl+C is safe)

This will create one node running Cassandra 3.11.2 as a master, and two worker nodes. You can get a description with `peg describe cassandra-cluster`.

## Manual administration
You can use `cqlsh` on the node to administer.

### Version
To check Cassandra version, `cqlsh` and then `show version`.

## Stopping when not in use
When you're not using the cluster, you can stop it temporarily to avoid being billed.

* Stop Cassandra: `peg service cassandra-cluster cassandra stop`
* Stop cluster: `peg stop cassandra-cluster` (answer y)

### Resuming
You have to start the services in the correct order:

* Start cluster: `peg start cassandra-cluster`
* Start Cassandra: `peg service cassandra-cluster cassandra start`

