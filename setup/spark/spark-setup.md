# Spark setup
* Set up [Pegasus](https://github.com/InsightDataScience/pegasus)
* Create master node: `peg up spark-master.yml`
	* You can create this from `spark-master-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Create worker nodes: `peg up spark-workers.yml`
	* You can create this from `spark-workers-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Fetch with `peg fetch spark-cluster`
* Install SSH: `peg install spark-cluster ssh`
* Install AWS credentials: `peg install spark-cluster aws`
* Install `bc` (hadoop won't install properly without it): `peg sshcmd-cluster spark-cluster "sudo apt install -y bc"`
* Hadoop is required for spark with Pegasus: `peg install spark-cluster hadoop`
* Finally Spark: `peg install spark-cluster spark`
* Now start both services:
	* `peg service spark-cluster hadoop start`
		* I don't know if starting hadoop is necessary, or if it should be started before spark.
	* `peg service spark-cluster spark start`
* You can access the Web UIs on `localhost` of your laptop by forwarding ports: 
	* Spark job web UI: `peg port-forward spark-cluster 1 4040:4040`
	* Spark cluster web UI: `peg port-forward spark-cluster 1 8080:8080`
	* Spark Jupyter web UI: `peg port-forward spark-cluster 1 8888:8888`
	* HDFS web UI: `peg port-forward spark-cluster 1 50070:50070`
	* Hadoop job tracker web UI: `peg port-forward spark-cluster 1 8088:8088`
	* Hadoop job history web UI: `peg port-forward spark-cluster 1 19888:19888`

This will create one node running Spark as a master, and two worker nodes. You can get a description with `peg describe spark-cluster`.

## Stopping when not in use
When you're not using the cluster, you can stop it temporarily to avoid being billed.

* Stop Spark: `peg service spark-cluster spark stop`
* Stop Hadoop: `peg service spark-cluster hadoop stop`
* Stop cluster: `peg stop spark-cluster` (answer y)

### Resuming
You have to start the services in the correct order:

* Start cluster: `peg start spark-cluster`
* Start Hadoop: `peg service spark-cluster hadoop start`
* Start Spark: `peg service spark-cluster spark start`

