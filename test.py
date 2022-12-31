import requests

with open("music_playlist\I want to be happy.mp3", 'rb')as test_file:
    test_file = test_file.read()
re = requests.post("http://127.0.0.1/APIs/blink_in",
                   files={'file': test_file})
print(re.text)

re = requests.get("http://127.0.0.1/APIs/blink_in",
                  params={'file': '2a2673e31f225f463dff5b989aab9b7e'})
with open('test.mp3', 'wb')as test:
    test.write(re.content)
