#!/usr/bin/env_python
import subprocess
import optparse
import re
import random


def get_arguments():
    """The function accepts arguments from the terminal"""
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC-address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC-address")
    (options, arguments) = parser.parse_args()
    return options


def change_mac(interface, mac):
    """The function changes the MAC-address in the terminal"""
    print("Changing MAC-address for " + interface + " to " + mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def get_current_mac(interface):
    """The function returns current MAC-address"""
    ifconfig_result = subprocess.check_output(["sudo", "ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))
    if mac_result:
        return mac_result.group(0)
    else:
        print("Could not read MAC-address")


def get_current_interface():
    """The function shows all interfaces in system"""
    ifconfig_result = subprocess.check_output(["sudo", "ifconfig"])
    interface_result = re.findall(r"\b\w+(?=:\s)", ifconfig_result.decode('utf-8'))
    if interface_result:
        return ", ".join(interface_result)
    else:
        print("Could not read interfaces")


def get_random_mac():
    """The function returns randomly generated MAC-address"""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


if __name__ == "__main__":
    args = get_arguments()
    print("Interfaces of this machine: " + get_current_interface())
    if args.interface is None:
        args.interface = input("Input interface: ")
    current_mac = get_current_mac(args.interface)
    print("Current MAC-address: " + str(current_mac))
    answer = input("Do you want to change MAC-address to random? (yes/no): ")
    if answer == 'yes':
        args.new_mac = get_random_mac()
        change_mac(args.interface, args.new_mac)
    elif answer == 'no':
        if args.new_mac is None:
            args.new_mac = input("Input MAC-address: ")
        change_mac(args.interface, args.new_mac)
    current_mac = get_current_mac(args.interface)
    if current_mac == args.new_mac:
        print("MAC-address was successfully changed to " + current_mac)
    else:
        print("MAC-address did not get changed")
