import requests

re = requests.post("http://localhost:5000/api/contacts", json = {"hola": "que tal"})