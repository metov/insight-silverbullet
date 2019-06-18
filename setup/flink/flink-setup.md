To install Flink:

* Set up [Pegasus](https://github.com/InsightDataScience/pegasus)
* Create master node: `peg up flink-manager.yml`
	* You can create this from `flink-manager-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Create worker nodes: `peg up flink-workers.yml`
	* You can create this from `flink-workers-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
			* You can also assign the security group after manually.
* Fetch with `peg fetch flink-cluster`
* Install SSH: `peg install flink-cluster ssh`
* Install AWS credentials: `peg install flink-cluster aws`
* Install `bc` (zookeeper won't install properly without it): `peg sshcmd-cluster flink-cluster "sudo apt install -y bc"`
* Hadoop is required for flink with Pegasus: `peg install flink-cluster hadoop`
* Finally Flink: `peg install flink-cluster flink`
* Now start both services:
	* `peg service flink-cluster flink start`
	* `peg service flink-cluster hadoop start`
		* I don't know if starting hadoop is necessary, or if it should be started before flink.
* Forward port so you can access Flink UI at localhost: `peg port-forward flink-cluster 1 8081:8081`
	* May give an error about "binary operator expected" at line 706 of `util.sh`, but `localhost:8081` should open as expected

This will create one node running Flink as a manager, and two worker nodes. You can get a description with `peg describe flink-cluster`.


