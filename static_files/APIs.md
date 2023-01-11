# HOME PAGE
home page now is basically a music/video music player with my personal favorite songs loaded. Chrome cannot user "," and "." to forward/backward video, and firefox cannot skip the appearing text by clicking... whatever, I guess that is due to broswer kernals' differences. 

http://blink-in.com

https://blink-in.com

# blink-in
for small file storage, not bigger than 18mb
```python
import requests

with open("music_playlist\I want to be happy.mp3", 'rb')as test_file:
    test_file = test_file.read()

# Uploading
re = requests.post("https://blink-in.com/APIs/blink_in",
                   files={'file': test_file})
# send binary data
print(re.text)
# {'content': ContentFile(path="2a2673e31f225f463dff5b989aab9b7e.png"), \
#   'commit': Commit(sha="d222298efe3f77304c9282fdc0cc2fe257388aae")}



#Downloading
re = requests.get("https://blink-in.com/APIs/blink_in",
                  params={'file': '2a2673e31f225f463dff5b989aab9b7e'})
#use path without .png to download file
with open('test.mp3', 'wb')as test:
    test.write(re.content)
# return raw data, you need to know the formating
```

# Cluster
a old toy I made about 2 years ago, hide your words/sentences in to "你好" (which is hello in chinese)

it is bsaically a static html with js, 

just go to https://blink-in.com/APIs/cluster or use request to see source code which is here, nothing very fancy at all

```python
re = requests.get("https://blink-in.com/APIs/cluster").text
print(re)
```

```html
<!DOCTYPE html>
<html>
<style>
    p {
        color: white;
        font-size: 50px;
        text-align: center;
    }

    div {
        text-align: center;
    }

    details {
        color: orange;
    }

    a {
        color: white;
    }

    .input {
        text-align: center;
    }

    .center-block {
        margin: auto;
        display: block;
    }
</style>

<head>
    <title>
        cluster
    </title>
</head>

<body style="background-color: black;">
    <h6 style="color: white;">Author:<a style="color: white;" href="https://github.com/DAF201">@DAF201</a></h6>
    <h6 style="color: white;">use the button to clear input box</h6>
    <h6 style="color: white;">Also, this is a very old toy made one or two years ago when I was starting with JS, I
        cannot guarentee it always work okay @01/10/2023</h6>
    <h6 style="color:white">the output string is basically "Hello" in chinese</h6>
    <p>Encode</p>
    <div>
        <p style="font-size:larger">input:</p>
        <input type='text' placeholder="what you want to hide" id='encode_input'>
        <button onclick='encode()'>submit</button>
        <br>
        <p style="font-size:larger">output:</p>
        <input type="text" placeholder="output will be here" id="encode_output">
        <button onclick="copy()">copy</button>
    </div>
    <br>
    <div>
        <button onclick='killbox()' style="scale: large;">Click me to clear the input box</button>
    </div>
    <br>
    <br>
    <div>
        <p>Decode</p>
        <p style="font-size:larger">input:</p>
        <input type="text" placeholder="paste what you have here" id='decode_input'>
        <button onclick="decode()">submit</button>
        <br>
        <h1 id='decode_output' style="color: white;"></h1>
    </div>
</body>
<script>
    'use strict'
    function encode() {
        const text_input = document.getElementById('encode_input').value;
        if (text_input.length != 0) {
            let temp = [];
            let fin = '你好';
            for (let i = 0; i < text_input.length; i++) {
                temp.push(text_input.charCodeAt(i).toString(2));
            }
            for (let i = 0; i < temp.length; i++) {
                temp[i] = temp[i].replace(/0/g, '‌');//8204 or U200C
                temp[i] = temp[i].replace(/1/g, '​');//8203 or U200B
            }
            for (let i = 0; i < text_input.length; i++) {
                fin = fin + temp[i] + '‍';//8205 or U200D
            }
            document.getElementById('encode_output').value = fin;
        }
    }
</script>
<script>
    'use strict'
    function decode() {
        const decode_text = document.getElementById('decode_input').value;
        if (decode_text.length != 0) {
            let temp = '';
            let output = ''
            for (let i = 0; i < decode_text.length; i++) {
                temp += decode_text[i];
            }
            temp = temp.split('好')[1];
            let data = '';
            let final = [];
            for (let i = 0; i < temp.length; i++) {
                if (temp.charCodeAt(i) == 8204) {
                    data += 0;
                }
                if (temp.charCodeAt(i) == 8203) {
                    data += 1;
                }
                if (temp.charCodeAt(i) == 8205) {
                    final.push(data);
                    data = '';
                }
            }
            for (let i = 0; i < final.length; i++) {
                final[i] = parseInt(final[i], 2);
                output += ('&#' + final[i]);
            }
            document.getElementById('decode_output').innerHTML = output;
        }
    }
</script>

<script>
    function copy() {
        let text_output = document.getElementById('encode_output');
        text_output.select();
        document.execCommand("copy");
    }
</script>
<script>
    function killbox() {
        document.getElementById('encode_input').value = '';
        document.getElementById('decode_input').value = '';
        document.getElementById('decode_output').innerHTML = '';
    }
</script>

</html>
```
