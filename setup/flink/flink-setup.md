Install Flink:

* Install JDK by running `setup-java.sh` on each EC2 to be used as Flink manager/workers.
* Set up passwordless SSH:
  * Run `setup-ssh.sh` on manager node
  * This will create `~/.ssh/id_rsa.pub`. Copy the contents of this file into `~/.ssh/authorized_keys` on each worker.
* Set up Flink:
  * Optional: Select mirror and version
    * Note that some other
    * Go to the [Flink download page](https://flink.apache.org/downloads.html).
    * Select the download link you want, copy the mirror URL.
    * Update `URL` variable in `setup-flink.sh`
  * Run `setup-flink.sh` on each machine
  * Edit Flink config on each node: `nano ~/flink-1.8.0/conf/flink-conf.yaml`
    * Path may differ if you picked a different Flink version
    * `jobmanager.rpc.address: MANAGER.NODES.PRIVATE.IP`
    * Optionally adjust the heapsizes to increase memory
  * On the manager, edit the slaves file: `sudo nano /usr/local/flink-1.8.0/conf/slaves`
    * Delete `localhost`
    * Add internal IPs of all worker nodes: 
      
      ```
        rm flink-1.8.0/conf/slaves
        echo '10.0.0.7' >> flink-1.8.0/conf/slaves
        echo '10.0.0.10' >> flink-1.8.0/conf/slaves
        echo '10.0.0.12' >> flink-1.8.0/conf/slaves
        echo '10.0.0.13' >> flink-1.8.0/conf/slaves
      ```
      
This will create 1 flink manager node and 4 worker nodes.
