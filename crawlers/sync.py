import requests 
import time

while True:
    print(requests.get("http://51.68.137.82:11111/dbToDjango/"))
    time.sleep(5)