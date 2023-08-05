#!/usr/bin/env python

import socket
from scapy.all import *

class Probe():
	def __init__(self, scanType, target, port, options):
		self.scan = scanType
		self.target = target
		self.port = port
		self.options = options
		
		self.recheck = False
		self.retryCt = self.options.retries
		
		self.srcPort = RandShort()
		self.result = ''
		
	def run(self):
		try:
			if self.scan == 'ack':
				self.result = sr1(IP(dst=self.target)/TCP(sport=self.srcPort, dport=self.port, flags="A"), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) == "<type 'NoneType'>"):
						return 0
					else:
						if(self.result.haslayer(TCP)):
							if(self.result.getlayer(TCP).flags == 0x4):
								return 1
						elif(self.result.haslayer(ICMP)):
							if(int(self.result.getlayer(ICMP).type) == 3 and int(self.result.getlayer(ICMP).code) in [1,2,3,9,10,13]):
								return 0
			
			if self.scan == 'fin':
				self.result = sr1(IP(dst=self.target)/TCP(sport=self.srcPort, dport=self.port, flags="F"), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) == "<type 'NoneType'>"):
						return 3
					else:
						if(self.result.haslayer(TCP)):
							if(self.result.getlayer(TCP).flags == 0x14):
								return -1
						elif(self.result.haslayer(ICMP)):
							if(int(self.result.getlayer(ICMP).type) == 3 and int(self.result.getlayer(ICMP).code) in [1,2,3,9,10,13]):
								return 0
		
			if self.scan == 'null':
				self.result = sr1(IP(dst=self.target)/TCP(sport=self.srcPort, dport=self.port, flags=""), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) == "<type 'NoneType'>"):
						return 3
					elif(self.result.haslayer(TCP)):
						if(self.result.getlayer(TCP).flags == 0x14):
							return -1
					elif(self.result.haslayer(ICMP)):
						if(int(self.result.getlayer(ICMP).type) == 3 and int(self.result.getlayer(ICMP).code) in [1,2,3,9,10,13]):	
							return 0
			
			if self.scan == 'syn':
				self.result = sr1(IP(dst=self.target)/TCP(dport=self.port, flags="S"), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) == "<type 'NoneType'>"):
						return 0
					else:
						if(self.result.haslayer(TCP)):
							if(self.result.getlayer(TCP).flags == 0x12):
								send_rst = sr(IP(dst=self.target)/TCP(dport=self.port, flags="R"), timeout=self.options.timeout, verbose=0)
								return 2
							elif (self.result.getlayer(TCP).flags == 0x14):
								return -1
						elif(self.result.haslayer(ICMP)):
							if(int(self.result.getlayer(ICMP).type) == 3 and int(self.result.getlayer(ICMP).code) in [1,2,3,9,10,13]):
								return 0
			
			if self.scan == 'tcp':
				self.result = sr1(IP(dst=self.target)/TCP(dport=self.port, flags="A"), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) == "<type 'NoneType'>"):
						return 0
					elif(self.result.haslayer(TCP)):
						if(self.result.getlayer(TCP).window == 0):
							return -1
						elif(self.result.getlayer(TCP).window > 0):
							return 1
		
			if self.scan == 'xmas':
				self.result = sr1(IP(dst=self.target)/TCP(sport=self.srcPort, dport=self.port, flags="FPU"), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) == "<type 'NoneType'>"):
						return 3
					elif(self.result.haslayer(TCP)):
						if(self.result.getlayer(TCP).flags == 0x14):
							return -1
					elif(self.result.haslayer(ICMP)):
						if(int(self.result.getlayer(ICMP).type)==3 and int(self.result.getlayer(ICMP).code) in [1,2,3,9,10,13]):	
							return 0
		
			if self.scan == 'udp':
				self.result = sr1(IP(dst=self.target)/UDP(dport=port), timeout=self.options.timeout, verbose=0)
				if self.result == None:
					self.recheck = True
				else:
					if(str(type(self.result)) != "<type 'NoneType'>"):
						return -1
					elif(self.result.haslayer(UDP)):
						return 1
					elif(self.result.haslayer(ICMP)):
						if(int(self.result.getlayer(ICMP).type) == 3 and int(self.result.getlayer(ICMP).code) == 3):
							return -1
						elif(int(self.result.getlayer(ICMP).type) == 3 and int(self.result.getlayer(ICMP).code) in [1,2,9,10,13]):
							return 0
		
			if self.recheck:
				self.retryCt = self.retryCt - 1
				if self.retryCt > 0:
					self.run()
				else:
					self.recheck = False

		except Exception as ex:
			print('Error testing port '+str(self.port)+'! '+str(ex))