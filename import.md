### 术语

* MTU Maximum Transmission Unit，最大传输单元

* jitter 网络抖动

* Bandwidth spike 带宽干扰

### 参数设置
* "-d", "--delay" Mean delay (in ms)

* "-v", "--variance" Delay variance (in ms)

* "-s", "--spikedelay" 带宽干扰启动延时， Bandwidth spike start delay (in sec), during which bandwidth drops to 


### 常数

* spikelength 带宽干扰时长 (in ms) 默认2000ms

* spikeDrop 带宽干扰时， 带宽下降的比率

* testFileSize 测试文件大小 33.6 MB (33,554,491 bytes) `/var/www/html/index.html`

### Tools

* tc netem + tbf configuration of local loopback interface. 
http://cizixs.com/2017/10/23/tc-netem-for-terrible-network

* Data captured with tcpdump, packet information stored.
http://linuxwiki.github.io/NetTools/tcpdump.html
http://dmdgeeker.com/post/tcpdump-basic-usage/

* Packet data analyzed with Python library matplotlib.
http://matplotlib.org/
https://liam0205.me/2014/09/11/matplotlib-tutorial-zh-cn/