import socket
import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def scanner_port(hote, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connexion:
            connexion.settimeout(0.5)
            connexion.connect((hote, port))
            return port
    except OSError:
        return None


def scan_ports(hote, ports, max_workers):
    start = time.time()
    print("Horaire :", now.strftime('%H:%M:%S'))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        resultats = executor.map(lambda p: scanner_port(hote, p), ports)
    ports_ouverts = sorted(p for p in resultats if p is not None)
    for port in ports_ouverts:
        print(f" ==> Le port {port} est ouvert")
    print("with thread :", time.time() - start, "secondes")
    return ports_ouverts

def dns_resolve(nom):
    try:
        ip = socket.gethostbyname(nom)
        print(f"Résolution DNS : {nom} ==> {ip}")
        return ip
    except socket.gaierror:
        print(f"Erreur : impossible de résoudre le nom '{nom}'")
        return None


### Main ###
if __name__ == "__main__":
    now = datetime.datetime.now().time()
    ports = range(1, 6000)
    max_workers = 200

    while(True):
        prompt= input("@ Saississez commande:") 

        match prompt:
            case "help" | "aide":
                print("[admin] dc         - pour de déconnecter")
                print("[admin] exit       - pour quitter le script")

            case "exit":
                print("EXIT...")
                quit(0)

            ### SCAN PORTS ###
            case "1":
                host = "10.184.18.225"
                print(f"\n=== Scan de {host} ===")
                scan_ports(host, ports, max_workers)
            
            ### SCAN DNS ###
            case "2":
                domaine = "scanme.nmap.org"
                host = dns_resolve(domaine)
                if host is None:
                   host = "pas d'ip trouvé"
                print(f"\n=== Scan de {domaine} ({host}) ===")
                scan_ports(host, ports, max_workers)
                
            case _:
                print("Veuillez utiliser une commande valide, ecrivez help pour lister les commandes")


## TODO
# DONE-  1. Scanner une IP spécifique
# 2. Scanner un nom de machine spécifique (DNS)
# 3. Scanner une plage d'adresses (Reverse DNS)
# 4. Scanner tout le réseau (avec ses sous réseaux et/ou ses vlan)
# 5. Calculer le temps d’exécution des diverses versions possibles
# 6. Ecrire dans journal d’activité résultat, horodaté (log)
# voir 10.184.0.0 - ESGI
# Script chat.server , si N client = N thread
# Pour chaque client > @ threads emission & reception
