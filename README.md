# blink-in_v0.0.2


API example(temp, will change in the future):

```python
import requests

with open("music_playlist\I want to be happy.mp3", 'rb')as test_file:
    test_file = test_file.read()
re = requests.post("http://blink-in.com/APIs/blink_in",
                   files={'file': test_file})
print(re.text)

re = requests.get("http://blink-in.com/APIs/blink_in",
                  params={'file': '2a2673e31f225f463dff5b989aab9b7e'})
with open('test.mp3', 'wb')as test:
    test.write(re.content)

```

rewriting with tornado

```shell
pip install requests, tornado, pillow, tornado_http_auth, pygithub
```

GUI REMOVED! APIs are in progress. Now using console to remote control

![](https://github.com/DAF201/blink-in_v0.0.2/blob/main/images/Screenshot%20(149).png)
![](https://github.com/DAF201/blink-in_v0.0.2/blob/main/images/Screenshot%20(150).png)
![](https://github.com/DAF201/blink-in_v0.0.2/blob/main/images/Screenshot%20(151).png)
