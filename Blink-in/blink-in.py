
from tools import *
from config import *
from html_pages import *
from flask import Flask, request, render_template, send_file, redirect, abort, send_from_directory
from base64 import b64encode, b64decode
from time import time, ctime
from hashlib import md5
from PIL import Image
from glob import glob
from itsdangerous import base64_decode, base64_encode
import json
import requests
import random
import string

app = Flask(__name__, static_folder='./static',
            template_folder='./templates')
app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static/', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


with open("./config/admin.json", "r")as admin_data:
    admin = json.load(admin_data)

with open("./config/black_list.json", "r")as black_list_data:
    black_list = json.load(black_list_data)

timing = {}
update_timer = time()


@app.before_request
def ip_check():

    global update_timer
    global black_list
    global timing
    if time()-update_timer > 300:
        update_timer = time()
        with open("./config/black_list.json", "r")as black_list_data:
            black_list = json.load(black_list_data)
        timing = {}

    ip = request.environ.get('REMOTE_ADDR')
    if ip in black_list:
        abort(403)
    else:
        if ip not in admin:
            if ip not in timing.keys():
                timing[ip] = 0
            else:
                timing[ip] = timing[ip]+1
                if timing[ip] >= 40:
                    black_list.append(ip)
                    with open("./config/black_list.json", "w")as black_list_data:
                        json.dump(black_list, black_list_data)
                    with open("./server_log/ban.txt", "a")as ban_log:
                        ban_log.write("@"+ctime(time())+'\t'+ip+'\n')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/blink-in')
def blink_in():
    return render_template('blink.html')


@app.route('/blink/blink_image_in', methods=["POST"])
def blink_image_in():
    clear_temp()
    clear_output()

    fail_list = []
    success_list = []
    image_list = []
    files = request.files.getlist('image')

    for file in files:
        file.save('./temporary/'+file.filename)
        image_list.append(file.filename)

    for image in image_list:
        blink_image_process(image)

    for file in glob('./output/*'):
        response = json.loads(image_upload(file))
        if response['code'] != 0:
            fail_list.append(file)
        else:
            success_list.append(base64_encode(response['data']['image_url'].split(
                'http://i0.hdslb.com/bfs/album/')[1].split('.png')[0].encode()).decode())

    return blink_result_page_1+','.join(success_list)+blink_result_page_2+','.join(fail_list)+blink_result_page_3


@app.route('/blink/blink_image_out', methods=["POST"])
def blink_links_in():
    clear_temp()
    clear_output()

    urls = request.form['text']

    try:
        urls = urls.replace('\r', '')
        urls = urls.replace('\n', '')
        if ',' in urls:
            urls = urls.split(',')
        else:
            urls = [urls]
    except:
        pass

    for url in urls:
        url = base64_decode(url).decode()
        url = 'http://i0.hdslb.com/bfs/album/'+url+'.png'
        image = Image.open(requests.get(url, stream=True).raw)
        image.save(temp+''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(6))+'.png')

    for image in glob(temp+'*'):
        url_image_process(image)

    result = ''
    for image in glob('./output/*'):
        with open(image, 'rb')as image:
            data = image.read()
            b64 = str(b64encode(data))[2:-1]
            result += '''<img src='data:image/jpg;base64,%s'><br>''' % b64
    return blink_image_result_page_1+result+blink_image_result_page_2


@app.route('/transcendence')
def transcendence():
    return render_template('transcendence.html')


@app.route('/transcendence/process', methods=["POST"])
def transcendence_process():
    clear_temp()
    clear_output()

    files = request.files.getlist('file')
    if str(files) != """[<FileStorage: '' ('application/octet-stream')>]""":
        for file in files:
            file.save('./temporary/'+file.filename)
            input_file = trans(file.filename)
            if (input_file == True):
                with open('./temporary/output.gif', 'rb')as output:
                    data = output.read()
                    b64 = b64encode(data).decode()
                return transcendence_return % b64
            else:
                file = max(glob("./output/*.*"), key=os.path.getctime)
                return send_file(file)
    else:
        return render_template('empty_input.html')


@app.route('/cluster')
def cluster():
    return render_template('cluster.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4123)
