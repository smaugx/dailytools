#!/bin/sh

which python3
if [ $? -eq 1 ]
then
    echo "no python3 found, will try to install python3"
    yum -y install wget &&
    yum -y groupinstall "Development tools" &&
    yum -y install zlib-devel libffi-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel &&
    wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz &&
    mkdir  /opt/python3 &&
    tar -xvJf  Python-3.7.2.tar.xz &&
    cd Python-3.7.2 &&
    ./configure --prefix=/opt/python3 &&
    make &&
    make install
    cd -
    
    ln -s /opt/python3/bin/python3 /usr/bin/python37
    ln -s /opt/python3/bin/pip3 /usr/bin/pip3
    yum -y install epel-release &&
    yum -y install python-pip
    ln -s /usr/bin/python37 /usr/bin/python3
    
    yum  install -y python-virtualenv.noarch
    
    rm -rf Python-3.7.2*
else
    echo 'check python3 ################################## Yes'
fi



