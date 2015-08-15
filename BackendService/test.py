import httplib2
import json

http = httplib2.Http()

body = {'USERNAME': 'foo', 'PASSWORD': 'bar'}
url = 'http://localhost:8080/check'
headers = {'Content-type': 'application/json'}
response, content = http.request(url, 'PUT', headers=headers, body=json.dumps(body))

headers = {'Content-type': 'application/json'}

url = 'http://localhost:8080/Agnivo'   
response, content = http.request(url, 'GET', headers=headers)
print content