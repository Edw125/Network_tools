#!/usr/bin/env_python
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import optparse


def scan(ip):
    """The function scans network"""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    package = broadcast / arp_request
    answered = srp(package, timeout=1)[0]
    clients = list()
    for i in answered:
        clients_param = {"ip": i[1][1].psrc, "mac": i[1][1].hwsrc}
        clients.append(clients_param)
    return clients


def print_clients(clients_list):
    """The function outputs discovered IP and MAC-addresses to the terminal"""
    print("IP\t\t\t\tMAC-address")
    print("-" * 50)
    for element in clients_list:
        print(element['ip'] + '\t' * 3 + element['mac'])


def get_arguments():
    """The function accepts arguments from the terminal"""
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="ip", help="Target IP-address or range of IP-addresses")
    (options, arguments) = parser.parse_args()
    return options


if __name__ == "__main__":
    args = get_arguments()
    if args.ip is None:
        args.ip = input("Enter IP-address or range of IP-addresses: ")
    print_clients(scan(args.ip))
