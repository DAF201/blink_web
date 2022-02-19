from tools import *
from config import *
from html_pages import *
from flask import Flask, request, make_response, render_template, send_file, send_from_directory, redirect
from base64 import b64encode, b64decode
from time import time, ctime
from PIL import Image
from glob import glob
import json
import requests
import random
import string
import datetime

app = Flask(__name__, static_folder='./static',
            template_folder='./templates')
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1000 * 20


@app.errorhandler(404)
def kill_bot(e):
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=90)
    if (request.cookies.get('admin') == None) or (request.cookies.get('admin')not in admin_cookie):
        ip = request.environ.get('REMOTE_ADDR')
        ban(ip)
        ban_response = make_response(render_template('ban.html'))
        ban_response.set_cookie(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
        return ban_response, 418
    else:
        return 'Page not found', 404


@app.errorhandler(404)
def login_killer(e):
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=90)
    if (request.cookies.get('admin') == None) or (request.cookies.get('admin')not in admin_cookie):
        ip = request.environ.get('REMOTE_ADDR')
        ban(ip)
        ban_response = make_response(render_template('ban.html'))
        ban_response.set_cookie(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
        return ban_response, 418
    else:
        return 'wrong method', 405


@app.errorhandler(413)
def up_load_over_size_file(e):
    return 'Maximum size 20mb'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static/', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


with open('./config/admin_cookie.json')as admin_cookie_data:
    admin_cookie = json.load(admin_cookie_data)

with open('./config/black_list.json', 'r')as black_list_data:
    black_list = json.load(black_list_data)

timing = {}
update_timer = time()


def update_info():

    global admin_cookie, black_list, timing, update_timer

    with open('./config/admin_cookie.json')as admin_cookie_data:
        admin_cookie = json.load(admin_cookie_data)

    with open('./config/black_list.json', 'r')as black_list_data:
        black_list = json.load(black_list_data)

    timing = {}
    update_timer = time()


def update_config():

    global param, cookie, enable_general_log, enable_admin_log, enable_ban_log, passcode, first_cover, second_cover, icon

    with open('./config/config.json', 'r')as config:
        config = json.load(config)
        param = config['param']
        cookie = config['cookie']
        enable_general_log = config['general_log']
        enable_admin_log = config['admin_log']
        enable_ban_log = config['ban_log']
        passcode = config['passcode']
        first_cover = config['first_cover']
        second_cover = config['second_cover']
        icon = config['icon']


def ban(ip, administrator='system'):

    global black_list
    if ip not in black_list:
        black_list.append(ip)
        with open('./config/black_list.json', 'w')as black_list_data:
            json.dump(black_list, black_list_data)
        if enable_ban_log:
            with open('./server_log/ban.txt', 'a')as ban_log:
                ban_log.write(str(ip).ljust(20) + 'ban at @\t' +
                              str(ctime(time()).ljust(20)) + ' by admin: ' + administrator + '\n')


def unban(ip, administrator):

    global black_list
    if ip in black_list:
        black_list.remove(ip)
        with open('./config/black_list.json', 'w')as black_list_data:
            json.dump(black_list, black_list_data)
        if enable_ban_log:
            with open('./server_log/ban.txt', 'a')as ban_log:
                ban_log.write(str(ip).ljust(20) + 'unban at @\t' +
                              str(ctime(time()).ljust(20)) + ' by admin: ' + administrator + '\n')


@app.before_request
def request_restrict():

    if time() - update_timer > 60:
        update_info()

    ip = request.environ.get('REMOTE_ADDR')
    login_cookie = request.cookies.get('admin')
    cookie_length = len(request.cookies.to_dict())

    if (login_cookie != None) and (login_cookie in admin_cookie):
        pass
    else:
        if (ip in black_list) or (cookie_length >= 1):
            return render_template('ban.html'), 418

        if ip not in timing.keys():
            timing[ip] = 0
        else:
            if timing[ip] > 40:
                ban(ip)
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(days=90)
                ban_response = make_response(render_template('ban.html'))
                ban_response.set_cookie(''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                        string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
                return ban_response, 418
            else:
                timing[ip] = timing[ip] + 1


@app.route('/login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        content = request.form['text']
        login_cookie = request.cookies.get('admin')
        if login_cookie in admin_cookie:
            if enable_general_log:
                with open('./server_log/general.txt', 'a')as general_log:
                    general_log.write('admin: cookie@: ' + str(login_cookie) + ' ip: ' + str(request.environ.get('REMOTE_ADDR')).ljust(20) + '\tat @'+str(ctime(time())).ljust(20) +
                                      '\tlogin in to control panel \n')
            return control_panel1 + str(param) + '<br>' + str(cookie) + '<br>admin log: ' + str(enable_admin_log) + '<br>ban log: ' + str(enable_ban_log) + '<br>general log: ' + str(enable_general_log) + '<br>passcode: ' + str(passcode) + '<br>' + control_panel2
        else:
            if content == passcode:
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(days=90)
                new_cookie = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(16))
                response = make_response(render_template('home.html'))
                response.set_cookie('admin', new_cookie, expires=expire_date)
                admin_cookie.append(new_cookie)
                if enable_admin_log:
                    with open('./server_log/admin.txt', 'a')as admin_log:
                        admin_log.write('adding new admin at @ ' +
                                        str(ctime(time())).ljust(20) + '\tip: ' + str(request.environ.get('REMOTE_ADDR')) + '\tcookie: ' + new_cookie.ljust(20) + '\n')
                with open('./config/admin_cookie.json', 'w')as admin_cookie_data:
                    json.dump(admin_cookie, admin_cookie_data)
                return response
        return render_template('ban.html')
    else:
        ban_response = make_response(render_template('ban.html'))
        ban_response.set_cookie(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
        return ban_response, 418


@app.route('/login/log_download', methods=['POST'])
def log_download():
    if (request.cookies.get('admin') == None) or (request.cookies.get('admin')not in admin_cookie):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        ip = request.environ.get('REMOTE_ADDR')
        ban(ip)
        ban_response = make_response(render_template('ban.html'))
        ban_response.set_cookie(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
        return ban_response, 418

    log_type = request.form.get('log')
    if enable_general_log:
        with open('./server_log/general.txt', 'a')as general_log:
            general_log.write('admin cookie: ' + request.cookies.get('admin') +
                              '\tdownloaded\t' + log_type + '\tat @' + str(ctime(time()).ljust(20)) + '\n')

    if log_type == 'admin':
        return send_file('./server_log/admin.txt', as_attachment=True)
    if log_type == 'ban':
        return send_file('./server_log/ban.txt', as_attachment=True)
    if log_type == 'general':
        return send_file('./server_log/general.txt', as_attachment=True)
    if log_type == 'cover1':
        return send_file(first_cover, as_attachment=True)
    if log_type == 'cover2':
        return send_file(second_cover, as_attachment=True)
    if log_type == 'icon':
        return send_file(icon, as_attachment=True)

    return 'log type can not be understand'


@app.route('/login/change_config', methods=['POST'])
def change_config():

    if (request.cookies.get('admin') == None) or (request.cookies.get('admin')not in admin_cookie):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        ip = request.environ.get('REMOTE_ADDR')
        ban(ip)
        ban_response = make_response(render_template('ban.html'))
        ban_response.set_cookie(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
        return ban_response, 418

    with open('./config/config.json', 'r')as config:
        config = json.load(config)

    config_type = request.form.get('config_type')
    config_value = request.form.get('config_value')
    old_config = ''

    if config_type == 'csrf':
        config['param'] = {'csrf': config_value}
        old_config = param
    if config_type == 'sessdata':
        config['cookie'] = {'SESSDATA': config_value}
        old_config = cookie
    if config_type == 'general_log':
        old_config = enable_general_log
        if config_value == 'false':
            config['general_log'] = False
        else:
            config['general_log'] = True
    if config_type == 'ban_log':
        old_config = enable_ban_log
        if config_value == 'false':
            config['ban_log'] = False
        else:
            config['ban_log'] = True
    if config_type == 'admin_log':
        old_config = enable_admin_log
        if config_value == 'false':
            config['admin_log'] = False
        else:
            config['admin_log'] = True

    with open('./config/config.json', 'w')as new_config:
        json.dump(config, new_config)

    if enable_general_log:
        with open('./server_log/general.txt', 'a')as general_log:
            general_log.write(
                'admin cookie: ' + request.cookies.get('admin') + ' ip ' + str(request.environ.get('REMOTE_ADDR')).ljust(20) + ' changed ' + config_type + ' from: ' + str(old_config) + ' to: ' + config_value + 'at time@ ' + ctime(time()).ljust(20) + '\n')

    update_config()

    return redirect('https://blink-in.ml/'), 302


@app.route('/login/server_update', methods=['POST'])
def server_update():

    if (request.cookies.get('admin') == None) or (request.cookies.get('admin')not in admin_cookie):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        ip = request.environ.get('REMOTE_ADDR')
        ban(ip)
        ban_response = make_response(render_template('ban.html'))
        ban_response.set_cookie(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
        return ban_response, 418

    server_config_type = request.form.get('server_config')
    server_config_value = request.files.get('file')
    if server_config_type == 'cover1':
        server_config_value.save('./static/cover1.png')
    if server_config_type == 'cover2':
        server_config_value.save('./static/cover2.png')
    if server_config_type == 'icon':
        server_config_value.save('./static/favicon.ico')
    if server_config_type == 'ban':
        ban(request.form.get('ip'), request.cookies.get('admin'))
    if server_config_type == 'unban':
        unban(request.form.get('ip'), request.cookies.get('admin'))

    update_config()

    return redirect('https://blink-in.ml/'), 302


#       above are server remote control
#       below are functions


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/blink-in')
def blink_in():
    return render_template('blink.html')


@app.route('/blink/blink_image_in', methods=['POST'])
def blink_image_in():
    clear_temp()
    clear_output()

    fail_list = []
    success_list = []
    image_list = []
    files = request.files.getlist('image')

    if str(files) != '''[<FileStorage: '' ('application/octet-stream')>]''':
        for file in files:
            # if file.filename.split('.')[1]not in ['png', 'jpeg']:
            #     expire_date = datetime.datetime.now()
            #     expire_date = expire_date + datetime.timedelta(days=90)
            #     ban(request.environ.get('REMOTE_ADDR'))
            #     ban_response = make_response(render_template('ban.html'))
            #     ban_response.set_cookie(''.join(random.choice(
            #         string.ascii_uppercase + string.digits) for _ in range(16)), ''.join(random.choice(
            #             string.ascii_uppercase + string.digits) for _ in range(16)), expires=expire_date)
            #     return ban_response, 418

            file.save('./temporary/' + file.filename)
            image_list.append(file.filename)

        for image in image_list:
            blink_image_process(image)

        for file in glob('./output/*'):
            response = json.loads(image_upload(file))
            if response['code'] != 0:
                fail_list.append(file)
            else:
                success_list.append(b64encode(response['data']['image_url'].split(
                    'http://i0.hdslb.com/bfs/album/')[1].split('.png')[0].encode()).decode())

        return blink_result_page_1 + ','.join(success_list) + blink_result_page_2 + ','.join(fail_list) + blink_result_page_3
    else:
        return render_template('empty_input.html')


@app.route('/blink/blink_image_out', methods=['POST'])
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

    try:
        for url in urls:
            url = b64decode(url.encode()).decode()
            url = 'http://i0.hdslb.com/bfs/album/'+url+'.png'
            image = Image.open(requests.get(url, stream=True).raw)
            image.save(temp + ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(6))+'.png')

        for image in glob(temp + '*'):
            url_image_process(image)

        result = ''
        for image in glob('./output/*'):
            with open(image, 'rb')as image:
                data = image.read()
                b64 = str(b64encode(data))[2:-1]
                result += '''<img src='data:image/jpg;base64,%s'><br>''' % b64
        return blink_image_result_page_1 + result + blink_image_result_page_2
    except Exception as e:
        print(e)
        return render_template('blink.html')


@app.route('/transcendence')
def transcendence():
    return render_template('transcendence.html')


@app.route('/transcendence/process', methods=['POST'])
def transcendence_process():
    clear_temp()
    clear_output()
    files = request.files.getlist('file')
    if str(files) != '''[<FileStorage: '' ('application/octet-stream')>]''':
        for file in files:
            file.save('./temporary/' + file.filename)
            input_file = trans(file.filename)
            if (input_file == True):
                with open('./temporary/output.gif', 'rb')as output:
                    data = output.read()
                    b64 = b64encode(data).decode()
                return transcendence_return % b64
            else:
                file = max(glob('./output/*.*'), key=os.path.getctime)
                return send_file(file)
    else:
        return render_template('empty_input.html')


@app.route('/cluster')
def cluster():
    return render_template('cluster.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=(
        r'C:\Certbot\live\blink-in.ml\cert.pem', r'C:\Certbot\live\blink-in.ml\privkey.pem'))
