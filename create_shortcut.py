#!/usr/bin/env python3
import os
import stat
import sys

def create_shortcut():
    # Chemin du script python actuel
    current_dir = os.getcwd()
    script_path = os.path.join(current_dir, "mac_changer.py")
    
    # Contenu du fichier .desktop
    # On utilise sh -c pour être plus générique que gnome-terminal si possible, 
    # mais pour ouvrir un terminal graphique, il faut invoquer le terminal.
    
    desktop_content = f"""[Desktop Entry]
Version=1.0
Name=MAC Changer Ecarlate
Comment=Change l'adresse MAC aléatoirement
Exec=gnome-terminal -- bash -c "sudo python3 '{script_path}'; echo; echo 'Appuie sur Entrée pour quitter...'; read line"
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;Application;
"""

    # Trouver le dossier Bureau
    home = os.path.expanduser("~")
    desktop_dirs = [os.path.join(home, "Bureau"), os.path.join(home, "Desktop")]
    target_dir = None
    for d in desktop_dirs:
        if os.path.exists(d):
            target_dir = d
            break
    
    if target_dir:
        file_path = os.path.join(target_dir, "MacChanger.desktop")
        try:
            with open(file_path, "w") as f:
                f.write(desktop_content)
            
            # Rendre exécutable
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)
            
            print(f"[+] Raccourci créé avec succès : {file_path}")
            print("-" * 50)
            print("[!] IMPORTANT :")
            print("1. Allez sur votre Bureau.")
            print("2. Faites un Clic Droit sur l'icône 'MAC Changer Ecarlate'.")
            print("3. Sélectionnez 'Autoriser le lancement' (Allow Launching) si l'option apparaît.")
            print("-" * 50)
        except Exception as e:
            print(f"[-] Erreur lors de la création du fichier : {e}")
    else:
        print("[-] Dossier Bureau non trouvé. Impossible de créer le raccourci automatiquement.")

if __name__ == "__main__":
    create_shortcut()
