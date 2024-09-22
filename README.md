# blink-in_v0.0.2

# I noticed the server was not that stable, but I assume that was because of my laptop is too old (2017 version samsung with 16GB mem)...

for usage, see [APIs](https://github.com/DAF201/blink-in_v0.0.2/blob/main/static_files/APIs.md)

now with https again:

[https://blink-in.com](https://blink-in.com)


AWS price increased a lot last year, I move it to my laptop which cannot pass certification, then I remove ssl.

API example (temporary, will change in the future):

```python
import requests

with open("music_playlist\I want to be happy.mp3", 'rb')as test_file:
    test_file = test_file.read()
re = requests.post("http://blink-in.com/APIs/blink_in",
                   files={'file': test_file})
print(re.text)
# {'content': ContentFile(path="2a2673e31f225f463dff5b989aab9b7e.png"), \
#   'commit': Commit(sha="d222298efe3f77304c9282fdc0cc2fe257388aae")}

re = requests.get("http://blink-in.com/APIs/blink_in",
                  params={'file': '2a2673e31f225f463dff5b989aab9b7e'})
with open('test.mp3', 'wb')as test:
    test.write(re.content)
# you will get raw data of this file 
# https://github.com/DAF201/blink-in_v0.0.2/blob/main/test.mp3
```

rewriting with tornado

required packages

```shell
pip install requests tornado pillow tornado_http_auth pygithub
```

Additionally you need to create a token.json in static_file folder

```json
{
    "token": "a github token",
    "repo": "a github inventory"
}
```

GUI REMOVED! APIs are in progress. Now using console to remote control

![](https://github.com/DAF201/blink-in_v0.0.2/blob/main/images/Screenshot%20(149).png)
![](https://github.com/DAF201/blink-in_v0.0.2/blob/main/images/Screenshot%20(150).png)
![](https://github.com/DAF201/blink-in_v0.0.2/blob/main/images/Screenshot%20(151).png)

"Don't try admin admin to login to console, I already changed the username and passsword"
