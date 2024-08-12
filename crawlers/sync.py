import requests 
import time

while True:
    requests.get("http://51.58.137.82:11111/dbToDjango/")
    time.sleep(5)