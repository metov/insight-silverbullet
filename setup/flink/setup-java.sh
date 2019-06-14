#!/bin/bash
# Installs Java 8, one of the requirements of Apache Flink.

# Update apt cache
sudo apt update

# Install Java 8
sudo apt install -y openjdk-8-jdk

# Configure Java paths
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

