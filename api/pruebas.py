import requests

re = requests.get("http://localhost:5000/api/user/wer/messages/sdfm")
print(re.json())