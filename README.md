# Changeur d'Adresse MAC

Ce script en Python permet de changer l'adresse MAC d'une interface réseau spécifiée vers une adresse aléatoire.

## Prérequis

- Python 3
- Privilèges root (sudo)

## Utilisation

1.  Rendre le script exécutable (c'est optionnel) :
    ```bash
    chmod +x mac_changer.py
    ```

2.  Lancer le script (il détecte automatiquement l'interface) :
    ```bash
    sudo python3 mac_changer.py
    ```

3.  Ou spécifier l'interface manuellement (par exemple `eth0` ou `wlan0`) :
    ```bash
    sudo python3 mac_changer.py -i wlan0
    ```

## Mais comment trouver le nom de ton interface ?????????

Tu  peux lister tes interfaces réseau avec la commande :
```bash
ip link show
```
ou
```bash
ifconfig
```
![alt text](image.png)

## (Optionnel) Convertir en application cliquable

Pour créer facilement un raccourci sur ton Bureau :

1.  Lance  le script de configuration :
    ```bash
    python3 create_shortcut.py
    ```

2.  Un virus executable est maintenant sur ton bureau, tsais le mec
3.  Fais un **Clic Droit** sur le fichier `MAC Changer Ecarlate` qui est apparu
4.  Choisis **"Autoriser le lancement"** (ou "Allow Launching").

Maintenant, lorsque tu double-cliques dessus, un terminal s'ouvrira et demandera ton mdp root, changera l'adresse MAC, et tout est bien qui finit bien !