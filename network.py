import socket

import infoports

iports = None

def ip_list_from_subnet(cidr: str) -> list:
    """ Retourne la liste des ip d'un sous-réseau au format cidr 
    
        :param cidr: sous-réseau au format cidr
        :return: liste des ip du sous-réseau
    """
    ip = subnet_from_ip(cidr)
    mask_int = int(cidr.split('/')[1])

    subnet_int = int(''.join([bin(int(grp))[2:].zfill(8) for grp in ip.split('.')]), 2)
    hosts_count = int(''.join(['0' if i < mask_int else '1' for i in range(32)]), 2)
    
    hosts = []
    for host in range(1, hosts_count):
        ip_int = subnet_int + host
        ip_bin = bin(ip_int)[2:].zfill(32)
        
        ip_list = [int(ip_bin[bit:bit+8], 2) for bit in range(0, 32, 8)]
        ip = '.'.join(str(grp) for grp in ip_list)
        hosts.append(ip)
        
    return hosts


def subnet_from_ip(cidr: str) -> list:
    """ Retourne l'adresse ip du sous-réseau à partir d'une adresse ip et d'un masque 
    
        :param cidr: adresse ip + masque au format cidr
        :return: adresse du sous-réseau
        
        
    """
    ip = cidr.split('/')[0]
    mask_cidr = int(cidr.split('/')[1])
    
    ip_int = int(''.join([bin(int(grp))[2:].zfill(8) for grp in ip.split('.')]), 2)
    mask_int = int(''.join(['1' if i < mask_cidr else '0' for i in range(32)]), 2)
    subnet_bin = bin(ip_int & mask_int)[2:].zfill(32)
    
    subnet_ip = '.'.join([str(int(subnet_bin[oct:oct+8], 2)) for oct in range(0, 32, 8)])
    return subnet_ip
    

def port_is_open(ip: str, port: int, display_result: bool = True) -> bool:
    """ Vérifie si un port est ouvert sur une adresse ip
    
        :param ip: adresse ip
        :param port: port à vérifier
        :param display_result: afficher le résultat
        :return: True si le port est ouvert, False sinon    
    """
    global iports
    
    if display_result and not iports:
        iports = infoports.InfoPorts()        
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        sock.connect((ip, port))
        if display_result:
            description = iports.description_for(port)
            print(f'Port {port} is open => {description}')
        return True
    except:
        pass
    sock.close()
    return False
    
    