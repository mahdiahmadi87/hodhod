import requests 
import time

while True:
    print(requests.get("http://51.58.137.82:11111/dbToDjango/"))
    time.sleep(5)