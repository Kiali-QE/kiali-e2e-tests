#!/bin/bash

HOME=`pwd`

# Install virtualenv, libcurl-devel, gcc, wget, unzip, openssl-devel
#yum install python-virtualenv wget unzip libcurl-devel unzip gcc openssl-devel redhat-rpm-config -y

# Setup virtual environment
virtualenv .kiali-qe-json
source .kiali-qe-json/bin/activate

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

rm -f chromedriver
wget https://chromedriver.storage.googleapis.com/2.28/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

