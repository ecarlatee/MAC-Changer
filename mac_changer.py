import subprocess
import argparse
import random
import re
import sys
import os

def print_banner():
    banner = r"""
  __  __          _____    _____ _                                  
 |  \/  |   /\   / ____|  / ____| |                                 
 | \  / |  /  \ | |      | |    | |__   __ _ _ __   __ _  ___ _ __  
 | |\/| | / /\ \| |      | |    | '_ \ / _` | '_ \ / _` |/ _ \ '__| 
 | |  | |/ ____ \ |____  | |____| | | | (_| | | | | (_| |  __/ |    
 |_|  |_/_/    \_\_____|  \_____|_| |_|\__,_|_| |_|\__, |\___|_|    
                                                    __/ |           
                                                   |___/            
    """
    print(banner)
    
    ecarlate_lines = [
        r"  ______               __      __       ",
        r" |  ____|             | |    | |      ",
        r" | |__   ___ __ _ _ __| | __ | |_ ___ ",
        r" |  __| / __/ _` | '__| |/ _` | __/ _ \ ",
        r" | |___| (_| (_| | |  | | (_| | ||  __/ ",
        r" |______\___\__,_|_|  |_|\__,_|\__\___| "
    ]
    
    # Kitsune (pourquoi pas ?)
    anime_lines = [
        r"      /\   /\       ",
        r"     /  \ /  \      ",
        r"    |  _   _  |     ",
        r"    | (o) (o) |     ",
        r"     \   ^   /      ",
        r"      \_____/       "
    ]
    
    # Jeune dégradé
    start_color = (255, 0, 0)
    end_color = (148, 0, 211)
    
    for i in range(len(ecarlate_lines)):
        line = ecarlate_lines[i]
        art = anime_lines[i] if i < len(anime_lines) else ""
        
        colored_line = ""
        length = len(line)
        for j, char in enumerate(line):
            if length > 1:
                ratio = j / (length - 1)
            else:
                ratio = 0
            
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            
            colored_line += f"\033[38;2;{r};{g};{b}m{char}"
        
        # Padding pour aligner l'art
        padding = " " * max(0, 45 - len(line))
        print(colored_line + "\033[0m" + padding + art)

    print("-" * 80)
    print("      by Ecarlate")
    print("-" * 80)

def get_arguments():
    parser = argparse.ArgumentParser(description="Changeur l'adresse MAC.")
    parser.add_argument("-i", "--interface", dest="interface", required=False, help="L'interface réseau (optionnel, détecté automatiquement si omis)")
    return parser.parse_args()

def get_active_interface():
    """Détecte l'interface réseau active (celle utilisée pour la route par défaut) ou la première disponible."""
    # 1. Essayer de trouver l'interface par défaut via la route (celle connectée à internet/réseau)
    try:
        route_result = subprocess.check_output(["ip", "route", "show", "default"], stderr=subprocess.DEVNULL).decode('utf-8')
        # Recherche de "dev <interface>"
        match = re.search(r"dev\s+(\S+)", route_result)
        if match:
            return match.group(1)
    except Exception:
        pass
    
    # 2. Si pas de route par défaut, lister toutes les interfaces et prendre la première qui n'est pas 'lo' (loopback)
    try:
        # Lister le dossier /sys/class/net est un moyen fiable sous Linux
        if os.path.exists("/sys/class/net"):
            interfaces = os.listdir("/sys/class/net")
            for iface in interfaces:
                if iface != "lo":
                    return iface
        
        # Fallback avec ip link si /sys/class/net n'est pas accessible (rare)
        ip_link_result = subprocess.check_output(["ip", "link", "show"]).decode('utf-8')
        matches = re.findall(r"^\d+:\s+(\S+):", ip_link_result, re.MULTILINE)
        for iface in matches:
            if iface != "lo":
                return iface
    except Exception:
        pass
        
    return None

def generate_random_mac():
    # Le premier octet doit être pair pour être une adresse unicast valide
    first_byte = random.randint(0x00, 0xff) & 0xfe
    mac = [
        first_byte,
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def change_mac(interface, new_mac):
    print(f"[+] Changement de l'adresse MAC pour {interface} vers {new_mac}")
    try:
        # Désac. l'interface
        subprocess.check_call(["sudo", "ip", "link", "set", "dev", interface, "down"])
        # Change l'adresse MAC
        subprocess.check_call(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac])
        # Réactive l'interface
        subprocess.check_call(["sudo", "ip", "link", "set", "dev", interface, "up"])
        print("[+] Adresse MAC changée.")
    except subprocess.CalledProcessError:
        print("[-] Erreur lors du changement de l'adresse MAC. Vérifiez que l'interface existe et que vous avez les droits root.")
    except Exception as e:
        print(f"[-] Une erreur inattendue est survenue : {e}")

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ip", "link", "show", interface]).decode('utf-8')
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print("[-] Impossible de lire l'adresse MAC.")
    except:
        print("[-] Impossible de lire l'adresse MAC.")
    return None

if __name__ == "__main__":
    print_banner()
    args = get_arguments()
    
    interface = args.interface
    
    if not interface:
        print("[*] Aucune interface spécifiée, recherche automatique...")
        interface = get_active_interface()
        if interface:
            print(f"[+] Interface trouvée : {interface}")
        else:
            print("[-] Impossible de détecter une interface réseau automatiquement.")
            print("[-] Veuillez spécifier une interface avec -i (ex: -i eth0)")
            sys.exit(1)
    
    current_mac = get_current_mac(interface)
    print(f"Adresse MAC actuelle : {str(current_mac)}")
    
    random_mac = generate_random_mac()
    change_mac(interface, random_mac)
    
    current_mac = get_current_mac(interface)
    if current_mac == random_mac:
        print(f"[+] Adresse MAC changée avec succès vers {current_mac}")
    else:
        print("[-] Le changement d'adresse MAC a échoué.")
