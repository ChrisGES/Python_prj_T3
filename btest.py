import socket
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
import ipaddress

def scanner_port(hote, port):
    try:
        # SOCK_STREAM = TCP
        # SOCK_DGRAM = UDP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connexion:
            connexion.settimeout(0.3)
            connexion.connect((hote, port))
            return port
    except OSError:
        return None

def scan_ports(hote, ports, max_workers):
    start = time.time()
    print("Horaire :", datetime.datetime.now().strftime('%H:%M:%S'))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # le lambda (fonction anonyme) fournit "hote" à scanner_port | map ne donne que "port" (contrainte de map)
        # map permet ;  (plus simple que submit)
        # 1 - de lancer la fonction en distribuant le travail sur le pool de threads
        # 2 - de collecter les valeurs renvoyées
        results = executor.map(lambda port: scanner_port(hote, port), ports)

    open_ports = sorted(port for port in results if port is not None)

    for port in open_ports:
        print(f" ==> Le port {port} est ouvert")

    print("with thread :", time.time() - start, "secondes")
    return open_ports

def dns_resolve(name):
    try:
        ip = socket.gethostbyname(name)
        print(f"Résolution DNS : {name} ==> {ip}")
        return ip
    except socket.gaierror:
        print(f"Erreur : impossible de résoudre le nom {name}")
        return None

def reverse_dns(ip):
    try:
        name = socket.gethostbyaddr(ip)[0]
        return name
    except socket.herror:
        return None

def scan_plage(plage_ip, max_workers):
    start = time.time()
    print("Horaire :", datetime.datetime.now().strftime('%H:%M:%S'))

    try:
        network = ipaddress.ip_network(plage_ip, strict=False)
    except ValueError:
        print(f"Erreur : '{plage_ip}' n'est pas un réseau valide")
        return []

    # Tranform 'IPv4Address' to 'string'
    ips = [str(ip) for ip in network.hosts()]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda ip: (ip, reverse_dns(ip)), ips)

    founds = [(ip, nom) for ip, nom in results if nom is not None]

    for ip, nom in founds:
        print(f" ==> {ip}  =>  {nom}")

    print("Reverse DNS terminé :", time.time() - start, "secondes")
    return None
    
### Main ###
if __name__ == "__main__":
    ports = range(1, 1000)
    max_workers = 200

    while(True):
        prompt= input("@ Saississez commande:") 

        match prompt:
            case "help" | "aide":
                print("exit       - pour quitter le script")
                print("1          - pour le scan d'une ip")
                print("2          - pour la resolution DNS")

            case "exit":
                print("EXIT...")
                quit(0)

            ### SCAN PORTS ###
            case "1":
                # host = "10.184.20.72"
                # host = "141.95.207.208"
                host = input("Entrez une ip : ")
                print(f"\n=== Scan de {host} ===")
                scan_ports(host, ports, max_workers)
            
            ### SCAN DNS ###
            case "2":
                #domaine = "scanme.nmap.org"
                domaine = input("Entrez le domaine : ")
                host = dns_resolve(domaine)
                if host is not None:
                    print(f"\n=== Scan de {domaine} ({host}) ===")
                    scan_ports(host, ports, max_workers)
                else:
                    print(f"Pas d'ip trouvé pour {domaine}")

            ### Reverse DNS ###
            case "3":
                plage_ip = "45.33.32.0/24" # scanme.nmap.org
                # plage_ip = "10.184.2.0/24" # esgi
                # plage_ip = input("Entrez la plage ip avec le masque : ")
                print(f"\n=== Reverse DNS de la plage {plage_ip} ===")
                scan_plage(plage_ip, max_workers)
            case _:
                print("Veuillez utiliser une commande valide, ecrivez help pour lister les commandes")


## TODO
# DONE-  1. Scanner une IP spécifique
# DONE-  2. Scanner un nom de machine spécifique (DNS)
# DONE-  3. Scanner une plage d'adresses (Reverse DNS)
# 4. Scanner tout le réseau (avec ses sous réseaux et/ou ses vlan)
# DONE-  5. Calculer le temps d’exécution des diverses versions possibles
# 6. Ecrire dans journal d’activité résultat, horodaté (log)
# Script chat.server , si N client = N thread
# Pour chaque client > @ threads emission & reception
# afficher les ports fermer 
# si du temps faire un mini menu pour filtrer le fichier de log en output
# rajouter juste le menuing du T1 et T2 pas besoin de fonctionnaliter 