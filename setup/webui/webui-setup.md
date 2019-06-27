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
	* Copy over the `web_ui.py` and dependencies: `peg scp to-rem webui 1 projects/insight-silverbullet/src/ silverbullet`
		* Edit `silverbullet/conf/cassandra.json` so that it reflects the internal IP of Cassandra master.

This node will host the Web UI, and can be opened to internet access, but it hsould be locked down with respect to the rest of the VPC. It only needs to fetch from the Cassandra (see remark above about security groups).

## To start the Web UI:
* Set Flask env.var: `export FLASK_APP=~/silverbullet/web_ui.py`
* Go to the script dir: `cd silverbullet` (Flask is a bit finicky about working dirs)
* You need to run with sudo to use port 80: `sudo python3 web_ui.py`
	* Ordinarily, it's bad to run Flask on 80. You should let Flask run on something like 5000, and use a proxy server like nginx to redirect 80 to that port. I did not have time to set that up for this project.
	* Web UI should now be accessible at the public IP of the node! To troubleshoot, you can `curl localhost` when SSH'd into the node.
