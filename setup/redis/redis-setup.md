To install Redis:

* Set up [Pegasus](https://github.com/InsightDataScience/pegasus)
* Create Redis node: `peg up redis.yml`
	* You can create this from `spark-master-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Fetch with `peg fetch redis`
* Install SSH: `peg install redis ssh`
* Install AWS credentials: `peg install redis aws`
* Finally Redis: `peg install redis redis`
	* Because we named the cluster "redis", it shows up twice in this command - once as in redis-the-node, once as in redis-the-software. Probably would be better to name it `redis-cluster` instead.
* Start: `peg service redis redis start`

This will create one node running Redis in cluster mode, but on a single node. You can get a description with `peg describe redis`. Because it's only one node, there is no practical benefit from cluster-mode, but in terms of developing against it it should behave almost identical to the "production" verison which would include multiple Redis masters and multiple Redis slaves. I have chosen to make it a single node due to limitations on number of AWS nodes and because Redis fault-tolerance is lower priority for this project.

With this Pegasus setup, Redis will not actually work because it has no slave nodes. Switch to standalone mode by editing `/usr/local/redis/redis.conf` and setting `cluster-enabled` to `no`. You will have to restart Redis: `peg service redis redis stop` and `peg service redis redis start`.

## Stopping when not in use
When you're not using the cluster, you can stop it temporarily to avoid being billed.

* Stop Redis: `peg service redis redis stop`
* Stop cluster: `peg stop redis` (answer y)

### Resuming
You have to start the services in the correct order:

* Start cluster: `peg start redis`
* Start Redis: `peg service redis redis start`
