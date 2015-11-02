#Lets build Statsite

Ensure that mock and git are installed

```
# yum --enablerepo=epel install mock git
# ln -s /etc/mock/epel-6-x86_64.cfg /etc/mock/default.cfg
```

Add a build user

```
# useradd -G mock build
```

Become the build user and clone this repo

```
# su - build
$ mkdir src && cd src
$ git clone https://github.com/mhollick/packagefactory.git
$ cd packagefactory/statsite-es
```

Build the RPM - this may take a while, especially the first time as packages are downloaded and cached.

```
$ make rpm
```

A post install action runs ```/etc/eurostar/emon-installer.sh``` this reads in a file from ```/etc/eurostar/default``` which should be of the format:

```
service=accounts
environment=int
role=appsvr
metricshost=1.1.1.1
loghost=2.2.2.2
```

If changes are made to the environment the detail file should be updated and the emon-installer re-ran.

##Disclaimer
This is not a final product.
The intent is to provide a single RPM file to configure base client monitoring.
When a private Yum repo is availible the configuruation will be split out into a seperate RPM.

