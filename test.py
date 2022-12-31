import requests

with open("test.py", 'rb')as test_file:
    test_file = test_file.read()
re = requests.post("http://127.0.0.1/APIs/blink_in",
                   files={'file': test_file}, params={'file_name': 'test.py'})
print(re.text)

# from src.tools import *
# with open('test1.png', 'rb')as test1:
#     data = test1.read()
# data = blink_in_decode(data)
# with open('testy.png', 'wb')as test_res:
#     test_res.write(data)
