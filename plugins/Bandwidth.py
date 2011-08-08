#!/usr/bin/python

import math, sys
from warnings import warn
from subprocess import *
from MirrorPlugin import MirrorPlugin

class Bandwidth(MirrorPlugin):

	def __init__(self, *args, **kwargs):
		if 'mirror' in kwargs:
			m = kwargs['mirror']
			super(Bandwidth, self).__init__(m)
			self.file = m.log_file
		elif 'filename' in kwargs:
			self.file = kwargs['filename']
		else:
			raise Exception
		
	def __before__(self, buff): pass

	def __after__(self, buff):
		bwsum = 0.0; min_bw = sys.maxint; max_bw = 0; n = 0
		# search for lines 'Downloaded: 2 files, 4.6K in 0s (93.0 KB/s)'
		command = 'grep Downloaded ' + self.file
		p = Popen(command, shell=True, bufsize=1024, stdin=PIPE, stdout=PIPE, close_fds=True)
		(child_stdin, child_stdout) = (p.stdin, p.stdout)

		for line in child_stdout:
			arr = line[:-1].split(" ")
			bw = float(arr[6][1:])
			unit = arr[7][0:-1]
			rbw = 0; n += 1
			if unit == "KB/s": rbw = bw
			elif unit == "MB/s": rbw = bw * 1024
			elif unit == "GB/s": rbw = bw * 1024**2
			else: warn("Unknown unit: " + unit)
			bwsum += rbw
			min_bw = min(rbw, min_bw)
			max_bw = max(rbw, max_bw)
			
		avg_bw = bwsum/n

		if not buff == None:
			buff.write('Min bw:\t%s KB/s\n' % (min_bw))
			buff.write('Avg bw:\t%s KB/s\n' % (avg_bw))
			buff.write('Max bw:\t%s KB/s\n' % (max_bw))
		
		return (min_bw, avg_bw, max_bw)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		(minbw, avg, maxbw) = Bandwidth(filename=filename).__execute__(None)
		print "bandwidth analysis for: " + filename
		print "min: " + str(minbw) + " KB/s"
		print "avg: " + str(avg) + " KB/s"
		print "max: " + str(maxbw) + " KB/s"
