import threading, encryption
from setup.setup_client import setup

settings = setup()
encryption.generate_keys(settings["dir"])