# Results

### Time series

![](../../res/time.png)

### delay

![](../../res/delay.png)

### bandwidth

![](../../res/bandwidth.png)

### packet loss

![](../../res/loss.png)

### Jitter

![](../../res/jitter_time.png)

![](../../res/jitter.png)

### Analysis

* At the cost of higher overhead, QUIC outperforms TCP in terms of time for transfer and average bandwidth used.
* When high delay, packet loss, and high bandwidth, QUIC will perform much better than TCP including time for transfer and throughput.
* Under favorable conditions, The QUIC will be more stable than TCP. You can see two picture in section Time series. 
* Under packet loss, QUIC also surpasses TCP.  When packet loss is 0%, throughput of QUIC is much higher than TCP. When packet loss is 5%, throughput of two protocol is very close, but QUIC is higher still.
* But when jitter happen, TCP can surpasses QUIC. Because the feature of the QUIC, QUIC can't handle the jitter better than TCP. It imply that QUIC is immature and not prefect.