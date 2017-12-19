# -*- coding: utf-8 -*-
"""
This script generates time series for the processed data extracted from the tests in the /processed folder
Change paths as needed. Run averaging.py before!
"""

import os
import collections

import numpy as np
import matplotlib.pyplot as plt

means = ['10', '50']
variances = ['0']
losses = ['0.0', '5.0']
bandwidths = ['100', '40', '5']
methods = ['quic', 'tcp']
spikes = ['0', '1']
testnumber = ['1', '2', '3', '4', '5']

pathfile = os.path.normpath('./processed/')
plotfolder = os.path.normpath('./plt/')

for mean in means:
	for variance in variances:
		for bandwidth in bandwidths:
			for loss in losses:

				for spike in spikes:
					mindex = 0
					dictionary = [
						collections.OrderedDict(), collections.OrderedDict()]
					err = False
					for method in methods:
						fichero = os.path.normpath(
							pathfile + '/AVGSUM' + method + '_' + bandwidth + '_' + loss + '_' + mean + '_' + variance + '_' + spike + '.txt')
						if spike == '1':
							try:
								with open(fichero, 'r') as f:
									for line in f:
										parts = line.split()
										dictionary[mindex][float(
											parts[0]) - 1.5] = float((float(parts[1]) * 16) / 1000000)
							except:
								err = True
								print('File AVGSUM' + method + '_' + bandwidth + '_' + loss +
									  '_' + mean + '_' + variance + '_' + spike + '.txt not found')

						else:
							try:
								with open(fichero, 'r') as f:
									for line in f:
										parts = line.split()
										# ATENCION!! *2 porque es bandwidth, 8 por bytes to bits
										dictionary[mindex][float(parts[0])] = float(
											(float(parts[1]) * 16) / 1000000)
							except:
								err = True
								print('File AVGSUM' + method + '_' + bandwidth + '_' + loss +
									  '_' + mean + '_' + variance + '_' + spike + '.txt not found')

						mindex += 1

					# plotting takes place
					vardelq = '0'
					varbwq = '0'
					fichero = os.path.normpath(
						pathfile + '/AVGDATAquic_' + bandwidth + '_' + loss + '_' + mean + '_' + variance + '_' + spike + '.txt')
					try:
						with open(fichero, 'r') as f:
							f.readline()
							line = f.readline()
							parts = line.split()
							vardelq = "{0:.3f}".format(
								round(float(parts[1]), 2))
							varbwq = "{0:.3f}".format(
								round(float(parts[2]), 2))
					except:
						err = True

					vardelt = '0'
					varbwt = '0'
					fichero = os.path.normpath(
						pathfile + '/AVGDATAtcp_' + bandwidth + '_' + loss + '_' + mean + '_' + variance + '_' + spike + '.txt')
					try:
						with open(fichero, 'r') as f:
							f.readline()
							line = f.readline()
							parts = line.split()
							vardelt = "{0:.3f}".format(
								round(float(parts[1]), 2))
							varbwt = "{0:.3f}".format(
								round(float(parts[2]), 2))
					except:
						err = True
					if not err:
						#                        longerlist=0 if (len(dictionary[0].keys())>=len(dictionary[1].keys())) else 1
						#                        shorterlist=(longerlist +1) %2
						#                        for key in dictionary[longerlist].keys():
						#                            if key not in dictionary[shorterlist].keys():
						#                                dictionary[shorterlist][key]=0

						plt.figure(figsize=(8, 5))
						t = np.arange(
							0, float(max(dictionary[0].keys())) + 0.5, 0.5)
						plt.plot(np.arange(float(min(dictionary[0].keys())), float(max(dictionary[0].keys(
						))) + 0.5, 0.5), dictionary[0].values(), "x-", linewidth=0.6, label="QUIC")
						plt.plot(np.arange(float(min(dictionary[1].keys())), float(max(dictionary[1].keys(
						))) + 0.5, 0.5), dictionary[1].values(), "x-", linewidth=0.6, label="TCP")
						plt.xlabel('Time in seconds')
						plt.ylabel('Throughput (Mbps)')
						plt.title('Throughput Comparison: Delay ' + mean + ' ms, Bandwidth ' + bandwidth + ' Mbps, PckLoss: ' + loss + '%, with ' + ('no ' if int(spike) == 0 else '') +
								  'spikes\n')
						plt.legend(bbox_to_anchor=(1.05, 1),
								   loc=2, borderaxespad=0.)
						rutafigura = os.path.normpath(
							plotfolder + '/BWPLOT_' + bandwidth + '_' + loss + '_' + mean + '_' + variance + '_' + spike + '.png')
						plt.savefig(rutafigura, dpi=150,
									bbox_inches='tight')  # , ,dpi=300
