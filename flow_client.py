from utilities.functions import *
from setup.setup_client import setup

settings = setup()
client_keys_exchange(ip = settings["ip"], root = settings["root"])

