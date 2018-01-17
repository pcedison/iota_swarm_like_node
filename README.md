# IOTA swarm-like Node
A IOTA swarm-like node proof of concepts (POC)

## Pre-Installation:
Dependency packages:

```$ sudo apt-get install python-pip python-setuptools python-dev python3-dev build-essential libssl-dev libffi-dev```

IOTA transaction POW utilities:

```
$ git clone https://github.com/chenweiii/dcurl.git
$ cd dcurl
$ git checkout task/nonce_searcher
$ make libdcurl.so
```

Official Python library for the IOTA Core:

```$ pip install pyota```
