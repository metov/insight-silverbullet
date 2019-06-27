# Web UI setup
* Set up [Pegasus](https://github.com/InsightDataScience/pegasus)
* Create master node: `peg up webui.yml`
	* You can create this from `webui-template.yml`, but you will need to fill in:
		* Subnet ID
		* Name of .pem file you would use to SSH into the instances
			* Only the filename, **without** the extension (.pem part)!
		* Security group
			* Multiple security groups are not supported!
			* I suggest making a single security group with all the rules for each of your clusters.
				* The security group should only be allowed to connect to the Cassandra master node on the correct port. For example, if Cassandra master was on 10.0.0.1, I would allow only outbound 10.0.0.1/32 on port 9042 in AWS.
			* You can also assign the security group after manually.
* Fetch with `peg fetch webui`
* Install SSH: `peg install webui ssh`
* Install AWS credentials: `peg install webui aws`
* Installing Flask is a bit involved, so it's better to SSH in: `peg ssh webui 1`
	* Update apt cache: `sudo apt update`
	* Install Python3 pip: `sudo apt install python3-pip`
	* Install Flask: `pip3 install Flask`
	* Install Cassandra driver: `pip3 install cassandra-driver`

This node will run the Web UI, and can be opened to internet access, but it hsould be locked down with respect to the rest of the VPC. It only needs to fetch from the Cassandra (see remark above about security groups).

Don't forget to edit `cassandra.json` to reflect the Cassandra internal IP!
