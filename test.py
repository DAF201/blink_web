import requests

re = requests.post("http://127.0.0.1/APIs/blink_in",
                   files=[('file', open('test.py', 'rb')), ('file', open('test.png', 'rb'))]).text
print(re)
