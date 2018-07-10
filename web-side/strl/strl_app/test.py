import requests
import json

url = 'http://127.0.0.1:8000/testrequest/'
something = {'some': 'data'}
r = requests.post(url, data=json.dumps(something))
print(r.text)
