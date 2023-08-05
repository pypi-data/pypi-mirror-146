#!/usr/bin/env python

class Utils:
	def iprange(self, addressrange):
		# converts a ip range into a list
		list=[]
		first3octets = '.'.join(addressrange.split('-')[0].split('.')[:3]) + '.'
		for i in range(int(addressrange.split('-')[0].split('.')[3]),int(addressrange.split('-')[1])+1):
			list.append(first3octets+str(i))
		return list
	
	def ip2bin(self, ip):
		b = ""
		inQuads = ip.split(".")
		outQuads = 4
		for q in inQuads:
			if q != "":
				b += self.dec2bin(int(q), 8)
				outQuads -= 1
		while outQuads > 0:
			b += "00000000"
			outQuads -= 1
		return b
	
	def dec2bin(self, n, d=None):
		s = ""
		while n>0:
			if n&1:
				s = "1"+s
			else:
				s = "0"+s
			n >>= 1
		if d is not None:
			while len(s)<d:
				s = "0"+s
		if s == "":
			s = "0"
		return s
	
	def bin2ip(self, b):
		ip = ""
		for i in range(0,len(b),8):
			ip += str(int(b[i:i+8],2))+"."
		return ip[:-1]
	
	def returnCIDR(self, c):
		parts = c.split("/")
		baseIP = self.ip2bin(parts[0])
		subnet = int(parts[1])
		ips=[]
		if subnet == 32:
			return self.bin2ip(baseIP)
		else:
			ipPrefix = baseIP[:-(32-subnet)]
			for i in range(2**(32-subnet)):
				ips.append(self.bin2ip(ipPrefix+self.dec2bin(i, (32-subnet))))
			return ips
	
	def urlValidator(x):
		try:
			result = urlparse(x)
			return all([result.scheme, result.netloc])
		except:
			return False