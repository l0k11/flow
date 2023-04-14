import socket, json, sqlite3, uuid, pathlib, os
from time import time

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')