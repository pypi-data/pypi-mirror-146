#!/usr/bin/env python

import math, threading, socket, random
from queue import Queue
from probe import Probe
from scapy.all import *
from scapy.all import TCP_SERVICES,UDP_SERVICES
from utils import Utils

class Portscan:
	def __init__(self, scanType, targetData, portData, resultsFrame):
		self.targets = []
		self.ports = []
		self.scanType = scanType
		self.resultsRoot = resultsRoot
		self.utils = Utils()
		
		self.timeout = 5
		self.threads = 10
		self.retries = 3
		
		self.queue = Queue()
		self.openPorts = []
		self.filteredPorts = []
		self.unfilteredPorts = []
		self.closed = 0
		
		self.current = None
		
		targets = targetData.split(',')
		for t in targets:
			t = t.strip()
			if '/' in t:
				valid = self.utils.urlValidator(t)
				if valid is not False:
					domain = valid.netloc
					target = socket.gethostbyname(domain)
					self.targets.append(target)
				else:
					ips = self.utils.returnCIDR(t)
					for ip in ips:
						self.targets.append(ip)
			elif '-' in t:
				ips = self.utils.iprange(t)
				for ip in ips:
					self.targets.append(ip)
			else:
				self.targets.append(socket.gethostbyname(t))
		
		if portsData == '' or portsData.lower() == 'basic':
			self.ports = list(range(1, 1025))
		elif portsData.lower() == 'all':
			self.ports = list(range(1, 65536))
		else:
			for x in portsData.split(','):
				self.ports.append(int(x.strip()))
		
		self.start = time.time()
	
	def worker(self):
		while not self.queue.empty():
			port = self.queue.get()
			result = self.scan(port)
			
			# closed port
			if result == -1:
				self.closed += 1
			
			# filtered port
			if result == 0:
				self.resultsRoot.display("Port "+str(port)+": Filtered")
			
			# unfiltered port
			if result == 1:
				self.resultsRoot.display("Port "+str(port)+": Unfiltered")
					
			# open port
			if result == 2:
				service = socket.getservbyport(p)
				self.resultsRoot.display('Port '+str(port)+': Open =>  '+service)
			
			# open|filtered port
			if result == 3:
				service = socket.getservbyport(p)
				self.resultsRoot.display("Port "+str(port)+": Open|Filtered => "+service)
	
	def scan(self, port):
		probe = Probe(self.scanType, self.current, port)
		return probe.run()
	
	def start(self):
		for target in self.targets:
			self.current = target
			random.shuffle(self.ports)
			self.resultsRoot.display(f"Preparing to scan {target}.")
			
			resp = sr1(IP(dst=target)/ICMP(), timeout=self.timeout, verbose=0)
			if resp == None:
				self.resultsRoot.display("This host is not responding. Exiting...")
)
				exit(1)
			
			for port in self.ports:
				self.queue.put(port)
			
			for t in range(self.threads):
				thread = threading.Thread(target=self.worker)
				thread_list.append(thread)
			
			for thread in thread_list:
				thread.start()
			
			for thread in thread_list:
				thread.join()
			
			self.resultsRoot.display(f'Scan of {target} complete.\r\n'))
		
		self.resultsRoot.display("All hosts scanned. Operation complete.")