#!/usr/bin/python

import math, sys
from subprocess import *
from plugin import MirrorPlugin

class BandwidthPlugin(MirrorPlugin):

	def __init__(self, logfile):
		self.logfile = logfile

	def __execute__(self):
		bwsum = 0.0; min_bw = 10000; max_bw = 0; n = 0
		# Downloaded: 2 files, 4.6K in 0s (93.0 KB/s)
		command = 'grep Downloaded ' + self.logfile
		p = Popen(command, shell=True, bufsize=1024, stdin=PIPE, stdout=PIPE, close_fds=True)
		(child_stdin, child_stdout) = (p.stdin, p.stdout)

		for line in child_stdout:
			n +=1
			arr = line[:-1].split(" ")
			nfiles = arr[1]
			size = arr[3]
			bw = arr[6][1:]
			unit = arr[7][0:-1]

			rbw = 0
			if unit == "MB/s":
				rbw = float(bw) * 1024
			elif unit == "KB/s":
				rbw = float(bw)
			else:
				print "what?: %s" % (unit)

			bwsum += rbw;
			min_bw = min(rbw, min_bw)
			max_bw = max(rbw, max_bw)

		return (min_bw, bwsum/n, max_bw)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		(minbw, avg, maxbw) = BandwidthPlugin(filename).__execute__()
		print "bandwidth analysis for: " + filename
		print "min: " + str(minbw) + " KB/s"
		print "avg: " + str(avg) + " KB/s"
		print "max: " + str(maxbw) + " KB/s"
