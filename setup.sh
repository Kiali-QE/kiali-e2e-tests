#!/bin/bash

HOME=`pwd`

yum install python-virtualenv  -y

# Setup virtual environment
virtualenv .kiali-qe-rest
source .kiali-qe-rest/bin/activate

# Install base requirements
pip install -r requirements.txt
pip install -U pip

## Begin - Install mgmtsystem

# Needed for RHEL7
cat /etc/os-release | grep -q "Red Hat Enterprise Linux"
if [ $? -eq "0" ]
then
    echo -e "\nInstalling RHEL dependencies..."
    pip install setuptools --upgrade
fi
