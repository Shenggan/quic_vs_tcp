#!/usr/bin/python
import argparse
import os
import os.path
import subprocess
import sys
import threading
import time
import collections

# Loopback interface mtu must be set to 1500
# sudo ifconfig lo mtu 1500
#
# IPv6 disabling on loopback:
# sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

# global variables definition

# misc
tests = 5
devnull = open(os.devnull, 'wb')
spikelength = 2000
spikeDrop = 0.1

# testfile stuff
testFile = "index.html"
testFilePath = "/var/www/html/" + testFile
tmpFilePath = "./testfile"
testFileQuicEssentials = "\"HTTP/1.1 200 OK\nX-Original-Url: https://www.example.org/\n\n\""
testFileGenerationCommand = "dd if=/dev/urandom of=" + \
	tmpFilePath + " bs=2M count=16 > /dev/null 2>&1"
testFileQuicIntroCommand = "echo " + testFileQuicEssentials + " | sudo tee " + testFilePath + \
	" > /dev/null && cat " + tmpFilePath + \
	" | sudo tee --append " + testFilePath + " >/dev/null"

testFileSize = 33554491

# netem commands
netemCommandDelete = "sudo tc qdisc del dev lo root"
netemCommandShow = "sudo tc qdisc show dev lo"
netemCommandRoot = "sudo tc qdisc add dev lo root handle 1: netem "
netemCommandLatencyAddendum = " delay xxxms"
netemCommandLatencyVarianceAddendum = " xxxms distribution normal"
netemCommandPacketLossAddendum = " loss xxx%"
netemCommandBandwidth = "sudo tc qdisc add dev lo parent 1: handle 2: tbf rate xxxmbit burst 256kbit latency 1000ms mtu 1500"
netemCommandChangeBandwidth = "sudo tc qdisc change dev lo parent 1: handle 2: tbf rate xxxmbit burst 256kbit latency 1000ms mtu 1500"

# spike indicating ping command
pingCommand = ["/bin/ping", "127.0.0.1", "-c", "1", "-s", "1"]

# client commands
tcpClientCommand = "wget -O ./tmp/index.html https://127.0.0.1/" + \
	testFile + " --no-check-certificate"
quicClientCommand = "/home/csg/software/proto-quic/src/out/Default/quic_client --host=127.0.0.1 --disable-certificate-verification --port=6121 https://www.example.org/ > ./tmp/download"
quicChromiumCommand = "google-chrome --user-data-dir=/tmp/chrome-profile --no-proxy-server --enable-quic --origin-to-force-quic-on=www.example.org:443 --host-resolver-rules='MAP www.example.org:443 127.0.0.1:6121' https://www.example.org/"
quicChromiumDownloadFilepath = "/home/csg/Downloads/download"

# tcpdump commands
pcapTouch = "touch /tmp/test.pcap"
tcpdumpCapture = ["/usr/bin/sudo", "/usr/sbin/tcpdump",
				  "-i", "lo", "-w", "/tmp/test.pcap"]
tcpdumpCaptureKill = "sudo kill "
tcpdumpAnalyze = "tcpdump -r /tmp/test.pcap -tttttnnqv > xxx 2>/dev/null"
tcpdumpSpikeFile = "/tmp/tcpdump.tmp"
tcpdumpSpikeAnalyze = "tcpdump -r /tmp/test.pcap -ttnnqv > " + \
	tcpdumpSpikeFile + " 2>/dev/null"


def main():
	parser = argparse.ArgumentParser(
		description="Execute a test file transfer on lo, with either QUIC or TCP+TLSv1.2, producing a packet dump. Network conditions can be specified.")
	parser.add_argument("-p", "--protocol", nargs="+", choices=[
		"TCP", "QUIC"], help="Protocol used in the transfer.", required="true")
	parser.add_argument("-l", "--packetloss", nargs="+", type=float, choices=[x * 0.1 for x in range(
		0, 51)], help="Packet loss as the probability an individual packet will be dropped", default="0")
	parser.add_argument("-d", "--delay", nargs="+", type=int,
						choices=range(10, 126), help="Mean delay (in ms)", default="10")
	parser.add_argument("-v", "--variance", nargs="+", type=int,
						choices=range(0, 51), help="Delay variance (in ms)", default="0")
	parser.add_argument("-b", "--bandwidth", nargs="+", type=int,
						choices=range(1, 101), help="Bandwidth (in Mbps)", default="100")
	parser.add_argument("-s", "--spikedelay", nargs="+", type=int, choices=range(0, 31),
						help="Bandwidth spike start delay (in sec), during which bandwidth drops to " + str(spikeDrop * 100) + "%", default="0")
	parser.add_argument(
		"--verbose", help="Generate more messages in the output.", action="store_true")
	parser.add_argument(
		"--vverbose", help="Generate even more messages in the output.", action="store_true")

	# parse arguments and create a params object for all possible combinations
	args = parser.parse_args()

	class params:
		def __init__(self, protocol, packetloss, delay, variance, bandwidth, spikedelay):
			self.protocol = protocol
			self.packetloss = packetloss
			self.delay = delay
			self.variance = variance
			self.bandwidth = bandwidth
			self.spikedelay = spikedelay
			self.spikelength = spikelength

	paramsQueue = collections.deque()

	if not isinstance(args.protocol, collections.Iterable):
		args.protocol = [args.protocol]
	if not isinstance(args.packetloss, collections.Iterable):
		args.packetloss = [args.packetloss]
	if not isinstance(args.delay, collections.Iterable):
		args.delay = [args.delay]
	if not isinstance(args.variance, collections.Iterable):
		args.variance = [args.variance]
	if not isinstance(args.bandwidth, collections.Iterable):
		args.bandwidth = [args.bandwidth]
	if not isinstance(args.spikedelay, collections.Iterable):
		args.spikedelay = [args.spikedelay]

	for protocol in args.protocol:
		for packetloss in args.packetloss:
			for delay in args.delay:
				for variance in args.variance:
					if variance >= delay:
						continue
					for bandwidth in args.bandwidth:
						for spikedelay in args.spikedelay:
							paramsQueue.append(
								params(protocol, packetloss, delay, variance, bandwidth, spikedelay))

	# function definitions

	# spike thread function

	def spikeThread(params):
		if params.bandwidth <= 8:
			netemCommandBandwidthReduce = netemCommandChangeBandwidth.replace(
				"xxx", str(1024 * params.bandwidth * spikeDrop))
			netemCommandBandwidthReduce = netemCommandBandwidthReduce.replace(
				"mbit", "kbit")
		else:
			netemCommandBandwidthReduce = netemCommandChangeBandwidth.replace(
				"xxx", str(params.bandwidth * spikeDrop))

		netemCommandBandwidthRestore = netemCommandChangeBandwidth.replace(
			"xxx", str(params.bandwidth))
		#netemCommandBandwidthRestore = netemCommandBandwidthRestore.replace("64kbit", "256kbit");

		time.sleep(params.spikedelay)
		#subprocess.Popen(pingCommand, stdout=devnull, stderr=devnull, shell=False);

		os.system(netemCommandBandwidthReduce)
		params.spikestart = startTime = time.time()

		if args.vverbose:
			print "Spike started:"
			print netemCommandBandwidthReduce

		time.sleep(params.spikelength / 1000)
		os.system(netemCommandBandwidthRestore)
		elapsedTime = time.time() - startTime
		if args.vverbose:
			print "Spike ended (duration: " + str(elapsedTime) + ", spikestart=" + str(params.spikestart) + ") :"
			print netemCommandBandwidthRestore

	# check test file
	def checkTestFile():
		if not os.path.isfile(testFilePath):
			return False
		if os.path.getsize(testFilePath) != testFileSize:
			return False

		return True

	# create the test file

	def generateTestFile():
		if args.verbose or args.vverbose:
			print "Generating test file..."
		retCode = os.system(testFileGenerationCommand)
		retCode2 = os.system(testFileQuicIntroCommand)

		if (retCode != 0) or (retCode2 != 0) or (not checkTestFile()):
			print >>sys.stderr, "Test file generation error (" + str(
				retCode) + ")."
			exit()

		#os.system("sudo cp -f " + testFilePath + " /var/www/html/");

		if args.verbose or args.vverbose:
			print "Test file created."
		return

	# configure netem

	def netemConfig(params):

		netemCommandConfigTmp = netemCommandRoot + \
			netemCommandLatencyAddendum.replace("xxx", str(params.delay))
		if params.variance > 0:
			netemCommandConfigTmp += netemCommandLatencyVarianceAddendum.replace(
				"xxx", str(params.variance))
		if params.packetloss > 0:
			netemCommandConfigTmp += netemCommandPacketLossAddendum.replace(
				"xxx", str(params.packetloss))
		netemCommandBandwidthTmp = netemCommandBandwidth.replace(
			"xxx", str(params.bandwidth))

		if args.vverbose:
			print "Configuring netem with following commands:"
			print "\t" + netemCommandDelete
			print "\t" + netemCommandConfigTmp
			print "\t" + netemCommandBandwidthTmp
			print

		os.system(netemCommandDelete)
		os.system(netemCommandConfigTmp)
		os.system(netemCommandBandwidthTmp)

		#netemCfg = commands.getoutput(netemCommandShow);
		# print netemCfg;

		return

	# generate output filename

	def getOutputFilename(testIndex, params):
		ret = str(params.protocol).lower()
		ret += "_" + str(params.bandwidth)
		ret += "_" + str(params.packetloss)
		ret += "_" + str(params.delay)
		ret += "_" + str(params.variance)
		if params.spikedelay > 0:
			ret += "_" + str(params.relspikestart)
		else:
			ret += "_0"
		ret += "_" + str(testIndex + 1)
		return ret

	# start tcpdump capture

	def startCapture():
		global captureProcess
		os.system(pcapTouch)
		captureProcess = subprocess.Popen(
			tcpdumpCapture, stdout=devnull, stderr=devnull, shell=False)
		if args.vverbose:
			print "Capture started (" + str(captureProcess.pid) + ")"
		return

	# stop tcpdump capture and run tcpdump analysis

	def stopCaptureAndAnalyze(testIndex, params):
		os.system(tcpdumpCaptureKill + str(captureProcess.pid))
		if args.vverbose:
			print "Analyzing pcap file..."

		if params.spikedelay > 0:
			os.system(tcpdumpSpikeAnalyze)
			mfile = open(tcpdumpSpikeFile)
			params.relspikestart = params.spikestart - \
				float(mfile.readline().split()[0])
			mfile.close()

		outputName = getOutputFilename(testIndex, params)

		os.system(tcpdumpAnalyze.replace("xxx", "./raw/"+ str(outputName)))

		return

	# create the test file if it does not already exist
	if not checkTestFile():
		generateTestFile()

	# run the tests for all params files

	while paramsQueue:
		params = paramsQueue.pop()

		if args.verbose:
			print "Running tests for: protocol=" + str(params.protocol) + ", packetloss=" + str(params.packetloss) + ", delay=" + str(params.delay) + ", variance=" + str(params.variance) + ", bandwidth=" + str(params.bandwidth) + ", spikedelay=" + str(params.spikedelay) + "."

		# configure netem
		netemConfig(params)

		# double the number of tests if a spike is present
		curTests = tests
		if params.spikedelay > 0:
			curTests *= 2
		#"main"
		for i in xrange(curTests):
			startCapture()
			if args.vverbose:
				print "Starting test #" + str(i + 1) + "..."

			# add spike thread if applicable
			if params.spikedelay > 0:
				threading.Thread(target=spikeThread, args=(params,)).start()

			# run the transfer
			if params.protocol == "TCP":
				os.system(tcpClientCommand)
			else:
				if os.path.isfile(quicChromiumDownloadFilepath):
					os.remove(quicChromiumDownloadFilepath)
				os.system(quicClientCommand)
				# while (True):
				#     if (not os.path.isfile(quicChromiumDownloadFilepath)):
				#         time.sleep(0.1)
				#         continue
				#     print os.path.getsize(quicChromiumDownloadFilepath);
				#     os.remove(quicChromiumDownloadFilepath)
				#     break

			stopCaptureAndAnalyze(i, params)

			if args.verbose or args.vverbose:
				outputName = getOutputFilename(i, params)
				print "Test #" + str(i + 1) + " finished, output in " + str(outputName)


main()
