#!/usr/bin/env python
import sys,os,re

class ip4:
        def __init__(self,inp):
                self.cidr=-1
                self.start=-1
                self.end=-1
                self.parseip(inp)



        def parseip(self,inp):
                self.ipversion=4
                self.bits=32
                self.ipsize=16777216
                self.bitl=256
                if inp.isdigit():
                        self.ip=int(inp)
                elif re.match('((?:\d+\.){3}\d+)$',inp):
                        n=re.match('((?:\d+\.){3}\d+)',inp)
                        self.ip=self.ip2dec(n.group(1))
                else:
                        n=re.match('((?:\d+\.){3}\d+)/(\d+)',inp)
                        self.ip=self.ip2dec(n.group(1))
                        self.cidr=int(n.group(2))
                        self.setstartend()


        def dec2bin(self,inp):
                c=2**self.bits
                b=""
                while c>=1:
                        if inp&c:
                                b+="1"
                        else:
                                b+="0"
                        c/=2
                return b

        def dec2ip(self,dec):
                ip=""
                s=self.ipsize
                while s>1:
                        n=dec/s
                        ip+="%d."%n
                        dec=dec-n*s
                        s/=self.bitl
                ip+="%d"%dec
                return ip



        def ip2dec(self,ip):
                ret=0
                s=self.ipsize
                for a in ip.split('.'):
                        ret+=int(a)*s
                        s/=self.bitl
                return ret


        def displaynet(self):
                if self.cidr!=-1:
                        bas=2**(self.bits-int(self.cidr))
                        netd=bas*int(int(self.ip)/bas)
                        return "%s/%d"%(self.dec2ip(netd),self.cidr)

        def setstartend(self):
                if self.cidr!=-1:
                        bas=2**(self.bits-self.cidr)
                        self.start=bas*int(self.ip/bas)
                        self.end=self.start+bas-1

        def getdec(self):
                return self.ip

        def getsize(self):
                if self.cidr==-1:
                        return 1
                else:
                        return self.end-self.start

        def getipversion(self):
                return self.ipversion

        def equals(self,a):
                if self.cidr == a.cidr and self.ipversion == self.ipversion:
                        if (self.cidr == -1):
                                if self.ip == a.ip:
                                        return True
                        else:
                                if self.displaynet() == a.displaynet():
                                        return True
                return False



        def ipinnet(self,ip):
                if self.cidr==-1:
                        return self.equals(ip)
                dec=ip.getdec()
                return dec >= self.start and dec <=self.end


        def getarpa(self):
                ip=self.dec2ip(self.ip)
                ret=""
                for a in ip.split('.'):
                        ret="%s.%s"%(a,ret)
                ret+="in-addr.arpa"
                return ret


        def __str__(self):
		if self.cidr==-1:
			return self.dec2ip(self.ip)
		else:
			return "%s/%s"%(self.dec2ip(self.ip),self.cidr)

if (len(sys.argv)<3):
	print >>sys.stderr,"Usage: %s smallip largeip"%sys.argv[0]
	sys.exit(1)

mmin=ip4(sys.argv[1])
mmax=ip4(sys.argv[2])

netblocks=[]

while mmin.getdec()<=mmax.getdec():
	cidr=0
	nr=ip4("%s/%s"%(mmin.__str__(),cidr))
	while (nr.start<mmin.getdec()):
		cidr+=1
		nr=ip4("%s/%s"%(mmin.__str__(),cidr))
	while (nr.end>mmax.getdec()):
		cidr+=1
		nr=ip4("%s/%s"%(mmin.__str__(),cidr))
	netblocks.append(nr)
	mmin=ip4(str(nr.end+1))
	cidr=0
	nr=ip4("%s/%s"%(mmin.__str__(),cidr))

for a in netblocks:
	print a
		
