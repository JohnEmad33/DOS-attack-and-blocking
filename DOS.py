import socket
from scapy.all import *
import scapy
from scapy.layers.inet import IP, UDP, TCP, ICMP
from datetime import datetime
import sys
import getopt
import subprocess

addresses = {}
time = {}
threshold = 20
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
s.bind(('', 80))
while 1:
    data, (ip_address, port) = s.recvfrom(2048)
    print(ip_address)


    # for k,v in list(time.items()):
    #     print ("K is   : " + k)
    #     if ((datetime.now() - v).total_seconds()) >= 60:
    #         addresses.pop(ip_address, None)
    #         time.pop(ip_address, None)

    if (ip_address in addresses.keys()):
        print(ip_address + " Entered ")
        addresses[ip_address] = addresses[ip_address] + 1
        print(addresses[ip_address])
        if addresses[ip_address] > threshold:
            subprocess.call(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])
            subprocess.call(["netfilter-persistent", "save"])
            print(ip_address, " is blocked successfully")

    else:
        addresses[ip_address] = 1
        time[ip_address] = datetime.now()
        print("saved")

    for k,v in list(time.items()):
        print("K is   : " + k)
        print("Before if   " , (datetime.now() - v).total_seconds())
        if ((datetime.now() - v).total_seconds()) >= 60:
            print("After if   " , (datetime.now() - v).total_seconds())
            addresses.pop(k, None)
            time.pop(k, None)

