import json
import urllib.request
import urllib.error

url = 'http://127.0.0.1:8000/api/register'
data = json.dumps({
    'email': 'testuser_new123456@example.com',
    'password': 'Password123!',
    'full_name': 'Test User New',
    'role': 'admin'
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    print('STATUS', resp.status)
    print(resp.read().decode())
except urllib.error.HTTPError as err:
    print('HTTP', err.code)
    print(err.read().decode())
except Exception as err:
    print('ERR', type(err).__name__, err)
