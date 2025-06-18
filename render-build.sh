#!/bin/bash
set -o errexit

# Install Java JDK
apt-get update
apt-get install -y openjdk-17-jdk

# Then run your normal build
pip install -r api/requirements.txt