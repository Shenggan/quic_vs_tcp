# Introduction

### What is QUIC

QUIC (Quick UDP Internet Connections) is a new transport protocol for the internet, developed by Google. It solves a number of transport-layer and application-layer problems experienced by modern web applications, while requiring little or no change from application writers.

![](../../res/quic.png)

### Key features
Key features of QUIC over existing TCP+TLS+HTTP2 include

* Dramatically reduced connection establishment time
* Improved congestion control
* Multiplexing without head of line blocking
* Forward error correction
* Connection migration

### Goals

Analyze performance of TCP and QUIC in terms of:

* Total transfer time
* Average Bandwidth used
* Overhead in bytes