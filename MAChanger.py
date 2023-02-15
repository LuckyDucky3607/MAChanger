#!/usr/bin/env python

import subprocess
import optparse
import re

parser = optparse.OptionParser()

parser.add_option("-d", "--default", dest="default", action="store_true", help="Reset the MAC to the default one")
parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="macaddr", help="The new MAC address you want to change to")
(options, arguments) = parser.parse_args()


def opt():

    if options.default:
        defu = subprocess.check_output("ethtool -P " + str(options.interface), shell=True)

        default_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(defu))

        subprocess.call("ifconfig " + options.interface + " down", shell=True)

        subprocess.call("ifconfig " + options.interface + " hw ether " + default_search.group(0), shell=True)

        subprocess.call("ifconfig " + options.interface + " up", shell=True)

        ifconfig = subprocess.check_output("ifconfig eth0", shell=True)

        def is_completed():
            new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
            if new_mac.group(0) == default_search.group(0):
                print("\n[+] MAC address have been restored to default successfully!")
            else:
                print("\n[-] MAC address did not change successfully please try again")
        is_completed()
    else:
        if not options.interface:
            parser.error("[-] Please enter an interface using -i use -h fore more info")

        if not options.macaddr:
            parser.error("[-] Please Enter a MAC address using -m use -h for more info")

        def mac_changer(interfa, newmac):

            subprocess.call("clear", shell=True)

            # print("\n\n[+] Changing MAC address for " + interfa + " to " + newmac + " ...\n\n")

            # killing the server
            subprocess.call(["ifconfig", str(interfa), "down"])

            # changing the macaddr
            subprocess.call(["ifconfig", str(interfa), "hw", "ether", str(newmac)])

            # restoring the interface
            subprocess.call(["ifconfig", str(interfa), "up"])

            # printing ifconfig
            subprocess.call("ifconfig " + str(interfa), shell=True)

        mac_changer(options.interface, options.macaddr)

        ifconfig_result = subprocess.check_output(["ifconfig", options.interface])

        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

        if mac_address_search_result:
            if mac_address_search_result.group(0) == options.macaddr:
                print("\n[+] Your MAC address have been changed successfully!")
                print("\n[!] Please note that changing your MAC address could restrict your connection run MAChanger.py -d -i {interface} to restore it to the default one")
            else:
                print("\n[-] Your MAC address could not be changed please try again")
        else:
            print("\n[-] Could not read MAC address")

    return options


try:
    opt()
except AttributeError:
    print("[-] Please select an interface with a MAC address")
    
