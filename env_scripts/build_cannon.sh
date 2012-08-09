#!/bin/sh

### Set up open file descriptor limits
sudo echo "fs.file-max = 1000000" >> /etc/sysctl.conf
sudo echo "ubuntu	soft	nofile	1000000" >> /etc/security/limits.conf
sudo echo "ubuntu	hard	nofile	1000000" >> /etc/security/limits.conf

### Add proper channels for nodejs
sudo apt-get -y install python-software-properties
sudo add-apt-repository -y ppa:chris-lea/node.js

### Update
sudo apt-get update

### Install
sudo apt-get -y install \
    build-essential \
    autoconf \
    automake \
    libtool \
    uuid-dev \
    git-core \
    nodejs \
    npm

git clone git://gist.github.com/3258447.git && cd 3258447
npm install

