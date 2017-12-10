# -*- coding: utf-8 -*-
"""
This script takes the output of script.py from the openPath folder, and processes
the files in order to extract only the data required (timestamp and bytes).
Output files saved to /processed
This script should be run after script.py
"""

import os
from os import listdir
from os.path import isfile, join

import collections
import re


def converttosec(tiempo):
	seconds = 0
	temp = tiempo[2].split('.')
	seconds = 60 * float(tiempo[1]) + float(temp[0]) + \
		(0.5 if int(temp[1]) >= 500000 else 0)
	if seconds < 0:
		seconds = 0.0
	return seconds


def actualizedict(dic, tiempo, pcks):
	if dic.has_key(tiempo):
		dic[tiempo] += pcks
	else:
		temp = tiempo - 0.5
		while (not dic.has_key(temp)) and temp >= 0:
			dic[temp] = 0
			temp -= 0.5
		dic[tiempo] = pcks
	return


openpath = os.path.normpath('./raw')
savepath = os.path.normpath('./processed')
onlyfiles = [os.path.normpath(openpath + '/' + f)
			 for f in listdir(openpath) if isfile(join(openpath, f))]
onlyfilessave = [savepath + '/' +
				 f for f in listdir(openpath) if isfile(join(openpath, f))]


for fich in onlyfiles:
	average_bandwidth = 0
	total_overhead = -32000000
	initial_time = 0
	final_time = 0
	bytesps = collections.OrderedDict()
	print "Processing file: " + fich
	with open(fich, 'r') as f:
		l = f.readline()
		div = l.split()
		# tiempo 0 horas, 1 minutos, 2 segundos, 3 milisegundos
		tiempo = div[0].split(':')
		tiempo2 = tiempo[2].split('.')
		initial_time = float(tiempo2[0]) + float(float(tiempo2[1]) / 1000000)
		actual_second = converttosec(tiempo)

		actualizedict(bytesps, float(actual_second), int(
			re.search(r'\d+', div[-1]).group()))
		total_overhead += bytesps[actual_second]
		f.next()
		last_actual = actual_second
		for line in f:
			try:
				div = line.split()
				tiempo = div[0].split(':')
			except:
				continue
			try:
				actual_second = converttosec(tiempo)
			except:
				actual_second = last_actual
			last_actual = actual_second
			if div[-1] == "[|ether]":
				continue
			try:
				pckbytes = int(re.search(r'\d+', div[-1]).group())
			except:
				print div
			actualizedict(bytesps, float(actual_second), pckbytes)
			total_overhead += pckbytes
			try:
				next(f)
			except:
				break

	temp = tiempo[2].split('.')
	final_time = float(tiempo[1]) * 60 + float(temp[0]
											   ) + float(float(temp[1]) / 1000000)
	rutasave = os.path.normpath(fich.replace(
		openpath + '/', savepath + '/SUM'))
	fichero = open(rutasave + '.txt', 'w')

	for key in sorted(bytesps.keys()):
		fichero.write(str(key) + ' ' + str(bytesps[key]) + '\n')
		average_bandwidth += float(bytesps[key] * 2)

	average_bandwidth = float(average_bandwidth / len(bytesps.keys()))
	fichero.close()
	rutasave = os.path.normpath(fich.replace(
		openpath + '/', savepath + '/DATA'))
	fichero = open(rutasave + '.txt', 'w')
	fichero.write(str(total_overhead) + ' ' + str(initial_time) +
				  ' ' + str(final_time) + ' ' + str(average_bandwidth))
	fichero.close()
