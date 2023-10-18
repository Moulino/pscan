#!/usr/bin/env python3

import optparse

import infoports
import network

PORT_DEFAULT_BEGIN = 1
PORT_DEFAULT_END = 65535

"""* ./pscan.py -t 192.168.1.0/24 -p 1-1000
* ./pscan.py -t 192.168.1.254 -p 80
* ./pscan.py -t 192.168.1.0/24 -p 80,443"""

parser = optparse.OptionParser("""
                               Usage: pscan.py -t <target> -p <ports>
                               Exemple: pscan.py -t 192.168.1.0/24 -p 1-1000
                                        pscan.py -t 192.168.1.254 -p 80
                                        pscan.py -t 192.168.1.0/24 -p 80,443
                                """)
parser.add_option('-t', '--target', dest="target", help="Adresse ip cible ou sous-réseau au format cidr")
parser.add_option('-p', '--ports', dest="ports", help="Ports à scanner -p 1-65535")
(options, args) = parser.parse_args()

ip_list = []
if options.target:
    if '/' in options.target:
        ip_list = network.ip_list_from_subnet(options.target.strip())
    else:
        ip_list.append(options.target.strip())
else:
    print('No target or subnet specified')
    exit(1)

ports = []  
if options.ports:
    if '-' in options.ports:
        begin_port = int(options.ports.split('-')[0])
        end_port = int(options.ports.split('-')[1])
        ports = range(begin_port, end_port+1)
    elif ',' in options.ports:
        ports = [int(p) for p in options.ports.strip().split(',')]
    else:
        ports = [int(options.ports.strip())]
        
    if type(ports) not in [list, range]:
        print('Invalid port range')
        exit(1)
else:
    ports = range(PORT_DEFAULT_BEGIN, PORT_DEFAULT_END+1)

iports = infoports.InfoPorts()

for ip in ip_list:
    
    print(f'Scanning {ip}...')

    for port in ports:
        network.port_is_open(ip, port)
    