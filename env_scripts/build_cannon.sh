#!/bin/sh

### Set up open file descriptor limits
echo "fs.file-max = 1000000" >> /etc/sysctl.conf
echo "ubuntu	soft	nofile	1000000" >> /etc/security/limits.conf
echo "ubuntu	hard	nofile	1000000" >> /etc/security/limits.conf

### Update
apt-get update

### Install
apt-get -y install \
    python-dev \
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
