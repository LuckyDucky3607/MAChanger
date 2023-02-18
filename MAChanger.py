#!/usr/bin/env python

import subprocess
import optparse
import re


def parsing():
    parser = optparse.OptionParser()

    parser.add_option("-d", "--default", dest="default", action="store_true", help="Reset the MAC to the default one")
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="macaddr", help="The new MAC address you want to change to")
    options = parser.parse_args()[0]
    if options.macaddr and options.default:
        parser.error("[-] Please only use -m or -d with -i can not be used in the same command use -h for more info")
    if not options.interface:
        parser.error("[-] Please enter an interface using -i use -h fore more info")
    if not options.default and not options.macaddr:
        parser.error("[-] Please Enter a MAC address using -m use -h for more info")
    return options


def default(option):
    if option.default:
        defu = subprocess.check_output("ethtool -P " + str(option.interface), shell=True)

        default_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(defu))
        if not default_search:
            print("\n[-] The specified interface does not have a MAC address or does not have a default one")
            exit()

        subprocess.call("ifconfig " + option.interface + " down", shell=True)

        subprocess.call("ifconfig " + option.interface + " hw ether " + default_search.group(0), shell=True)

        subprocess.call("ifconfig " + option.interface + " up", shell=True)

        ifconfig = subprocess.check_output("ifconfig " + option.interface, shell=True)

        new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
        if new_mac.group(0) == default_search.group(0):
            print("\n[+] MAC address have been restored to default successfully!")
            exit()
        else:
            print("\n[-] MAC address did not change successfully please try again")
            exit()


def mac_changer(interfa, newmac):
    subprocess.call("clear", shell=True)

    print("\n[+] Changing MAC address for " + str(interfa) + " to " + str(newmac) + " ...\n\n")

    # killing the server
    subprocess.call(["ifconfig", str(interfa), "down"])

    # changing the macaddr
    subprocess.call(["ifconfig", str(interfa), "hw", "ether", str(newmac)])

    # restoring the interface
    subprocess.call(["ifconfig", str(interfa), "up"])

    # printing ifconfig
    subprocess.call("ifconfig " + str(interfa), shell=True)


def opt(option):
    ifconfig_result = subprocess.check_output(["ifconfig", option.interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        if mac_address_search_result.group(0) == option.macaddr:
            print("\n[+] Your MAC address have been changed successfully!")
            print("\n[!] Please note that changing your MAC address could restrict your connection to the internet run python MAChanger.py -d -i {interface} to restore it to the default")
        else:
            print("\n[-] Your MAC address could not be changed please try again")
    else:
        print("\n[-] Could not read MAC address")


option_s = parsing()
default(option_s)
mac_changer(option_s.interface, option_s.macaddr)
opt(option_s)

