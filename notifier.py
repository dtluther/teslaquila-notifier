import requests

resp1 = requests.get("https://teslatequila.tesla.com/")

if "out of stock" not in resp1.text.lower():
    print("IN STOCK")
else:
    print("NO LUCK")
