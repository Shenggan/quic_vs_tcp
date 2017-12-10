# QUIC vs TCP

A Survey and Benchmark of QUIC. 

## Introduction

### What is QUIC

### Goals

Analyze performance of TCP and QUIC in terms of:

* Total transfer time
* Average Bandwidth used
* Overhead in bytes

## Methods

### Experimental Setup

#### Overview

A 33.6 MB testfile `index.html` will generate in `/var/www/html/` and we will get it from *quic server* and *apache2 server* with *quic client* and *wget*. The protocal two way used is **QUIC** and **TCP**. And we will run the experiments under difference network enviroments.

For practical, we will use simulate enviroment in **local**. We use *tc netem* and *tbf* to config local loopback interface.

![](./res/struct.png)

#### Compile Chromium

Because of the quic protocal is embedded in Chromium, so we must build our *quic_server* and *quic_client* from the source of Chromium.

#### Apache2 Server

We will test TCP with Apache2 Server, to be closer to the reality world, we config the server with TLS. 

#### Prepare for Experiments

Before we start the experiments, we need finished this four steps:

1. Set loopback interface mtu to 1500
1. IPv6 disabling on loopback
1. Start Apache2 Server
1. Start QUIC Server

See detail in [env_setup.sh](./scripts/env_setup.sh).

### Run and Analyse

#### Usage

```shell
./scripts/env_setup.sh
./scripts/run,sh
./scripts/analyse.sh
```

#### Generate raw data

#### Data Analysis

#### Visualization

## Results

## Conclusions

## Future Work

## Referance

1. http://cizixs.com/2017/10/23/tc-netem-for-terrible-network
1. http://linuxwiki.github.io/NetTools/tcpdump.html
1. http://dmdgeeker.com/post/tcpdump-basic-usage/
1. http://matplotlib.org/
1. https://liam0205.me/2014/09/11/matplotlib-tutorial-zh-cn/
