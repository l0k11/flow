import art
from functions.setup import client_setup

settings = client_setup()
print(settings["server"])
print(settings["root"])

print(art.text2art("Welcome    to"))
print(art.text2art("flow", font='block'))