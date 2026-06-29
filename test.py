#scan de port
import socket  
import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# https://towardsdev.com/whats-the-best-way-to-handle-concurrency-in-python-threadpoolexecutor-or-asyncio-85da1be58557

now1 = datetime.datetime.now().time() 
print("Horaire :", now1.strftime('%H:%M:%S'))
hote = "127.0.0.1"
#hote = "10.184.18.225"

### Functions ###
def scanner_port(port):
    try:
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.settimeout(0.5)
        connexion.connect((hote, port))
        with verrou_pool:
            ports_ouverts_pool.append(port)
    except socket.error:
        pass
    finally:
        connexion.close()

def scan_ports(hote, ports, max_workers):
    """Scanne une plage de ports d'un hôte. Retourne la liste des ports ouverts."""
    Start3 = time.time()
    ports_ouverts = []
    verrou = threading.Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda port: scanner_port(hote, port, ports_ouverts, verrou), ports)

    for port in sorted(ports_ouverts):
        print(f" ==> Le port {port} est ouvert")

    End3 = time.time()
    print("with thread :", End3 - Start3, "secondes")
    return sorted(ports_ouverts)

print("\n===OG ver===")
Start3 = time.time()
ports_ouverts_pool = []
verrou_pool = threading.Lock()

# To check nb threads avalaible : sysctl kern.num_taskthreads
with ThreadPoolExecutor(max_workers=200) as executor:
    executor.map(scanner_port, range(1, 1000))

for port in sorted(ports_ouverts_pool):
    print(f" ==> Le port {port} est ouvert")

End3 = time.time()
print("with thread :", End3-Start3, "secondes")




## TODO
# DONE-  1. Scanner une IP spécifique
# 2. Scanner un nom de machine spécifique (DNS)
# 3. Scanner une plage d'adresses (Reverse DNS)
# 4. Scanner tout le réseau (avec ses sous réseaux et/ou ses vlan)
# 5. Calculer le temps d’exécution des diverses versions possibles
# 6. Ecrire dans journal d’activité résultat, horodaté (log)


# print ("2 test")
# Start = time.time()
# for port in range (1, 65535): ## 135 RPC
#     try :      
#         connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         connexion_principale.connect((hote, port))         
#         print(" ==> Le port:",port," est ouvert")
       
#     except: #socket.error:
#         print ("Le port:",port, "est fermé")
#     connexion_principale.close()
 
# End = time.time() ### fin du scan



# print("no :",End-Start,"secondes") 