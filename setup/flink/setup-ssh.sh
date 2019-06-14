#!/bin/bash
# Create passwordless SSH key so that Flink manager can talk to Flink worker nodes.

# Update apt cache
sudo apt update

# Install SSH server
sudo apt install -y openssh-server openssh-client

# Create keypair
ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa

