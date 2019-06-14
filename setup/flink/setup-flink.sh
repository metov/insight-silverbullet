#!/bin/bash
# Install Flink. Change this URL if you want a different mirror or version.
URL="ftp://apache.cs.utah.edu/apache.org/flink/flink-1.8.0/flink-1.8.0-bin-scala_2.11.tgz"

# Parse out the filename; see http://mywiki.wooledge.org/BashFAQ/100#Removing_part_of_a_string
FILENAME=${URL##*/}

# Download flink
wget $URL

# Extract
#sudo tar xzf $FILENAME -C /usr/local/
tar xzf $FILENAME

# Set manager IP (watch out for bash's finnicky quote logic here)
MANAGER='10.0.0.6'
sed -i -e "s/jobmanager.rpc.address: localhost/jobmanager.rpc.address: $MANAGER/g" ~/flink-1.8.0/conf/flink-conf.yaml

