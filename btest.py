import socket
import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def scanner_port(hote, port, ports_ouverts, verrou):
    try:
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.settimeout(0.5)
        connexion.connect((hote, port))
        with verrou:
            ports_ouverts.append(port)
    except socket.error:
        pass
    finally:
        connexion.close()


def scan_ports(hote, ports, max_workers):
    Start3 = time.time()
    ports_ouverts = []
    verrou = threading.Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda port: scanner_port(hote, port, ports_ouverts, verrou), ports)

    for port in sorted(ports_ouverts):
        print(f" ==> Le port {port} est ouvert")

    End3 = time.time()
    print("with thread :", End3 - Start3, "secondes")
    #return sorted(ports_ouverts)
    return


### Main ###
if __name__ == "__main__":
    hote = "127.0.0.1"
    ports = range(1, 1000)
    max_workers = 200

    now = datetime.datetime.now().time()
    print("Horaire :", now.strftime('%H:%M:%S'))
    print(f"\n=== Scan de {hote} ===")
    
    #resultat = scan_ports(hote, ports, max_workers)
    scan_ports(hote, ports, max_workers)

## TODO
# DONE-  1. Scanner une IP spécifique
# 2. Scanner un nom de machine spécifique (DNS)
# 3. Scanner une plage d'adresses (Reverse DNS)
# 4. Scanner tout le réseau (avec ses sous réseaux et/ou ses vlan)
# 5. Calculer le temps d’exécution des diverses versions possibles
# 6. Ecrire dans journal d’activité résultat, horodaté (log)