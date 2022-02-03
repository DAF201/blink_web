from cv2 import norm
from flask import request, render_template, Flask, send_file, redirect, abort, send_from_directory
import os
import base64
import time
from data import *
from tools import *
import hashlib

app = Flask(__name__, static_folder='./temp',
            template_folder='./templates')

app.config['TRAP_HTTP_EXCEPTIONS'] = True


'''start up, timing, admin list, and black list'''

ip_timing = {}

with open('privilege_list.json', 'r')as privilege:
    privilege = json.load(privilege)

with open('ban_list.json', 'r')as ip_list:
    ip_ban_list = json.load(ip_list)


@app.route('/favicon.ico')
def favicon():
    '''handle icon'''

    return send_from_directory(os.path.join(app.root_path, 'template'),
                               'something.ico', mimetype='image/vnd.microsoft.icon')


@app.before_request
def block():
    '''block ip when it request too fast'''

    ip = request.environ.get('REMOTE_ADDR')

    if ip not in privilege and request.url.split('/')[-1] != 'favicon.ico':
        '''how to disable this stupid favicon request...'''

        '''is amdin?ignore:timing'''

        if ip not in ip_timing.keys():

            '''first time?Add to timing list:check interval'''
            ip_timing[ip] = time.time()

        else:

            if time.time()-ip_timing[ip] < (random.randrange(0, 1)/10):

                if ip not in ip_ban_list:

                    '''request too fast and not in ban list->add to ban list'''
                    with open('ban_list.json', 'w')as ip_list:
                        ip_ban_list.append(ip)
                        json.dump(ip_ban_list, ip_list)

                    '''create banning log'''
                    with open('banning_log.txt', 'a')as log:
                        log.write(ip+'\t'+time.ctime(time.time())+'\n')

            else:
                '''update last request time'''
                ip_timing[ip] = time.time()

        if ip in ip_ban_list:

            abort(403)


@app.route('/')
def home():
    '''Home page'''

    clean_temp()

    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    '''admin login'''

    clean_temp()

    user = request.form['text']
    with open('admin.json')as admin:
        admin = json.load(admin)

    '''check passcode MD5'''
    if hashlib.md5(user.encode()).hexdigest() in admin:

        ip = request.environ.get('REMOTE_ADDR')

        '''new admin adding'''
        if ip not in privilege:

            privilege.append(ip)

            '''log and update'''
            with open('normal_log.txt', 'a')as normal_log:
                normal_log.write('adding new admin: %s @%s',
                                 (ip, time.ctime(time.time)))

            with open('privilege_list.json', 'w')as privilege_list:
                json.dump(privilege, privilege_list)

        '''get files in DL folder'''
        files = os.listdir(downloads_path)
        page_content = ''

        '''add files list to HTML'''
        for file in files:
            file = os.path.basename(file)

            '''ignore system file'''
            if file not in ['~$D-220 Command List-V1.1.docx', 'desktop.ini']:
                page_content += '<p>%s</p>' % file

        return download_page_part1 % hashlib.md5(user.encode()).hexdigest()+page_content+download_page_part2

    else:

        return render_template('permission_denied.html')


@app.route('/clear_up', methods=['POST'])
def clear_up():

    clean_temp()

    try:

        user = request.form['user']
        with open('admin.json')as admin:
            admin = json.load(admin)

        if user in admin:

            files = os.listdir(downloads_path)

            for file in files:
                file = os.path.basename(file)

                '''don't clear system file'''
                if file not in ['~$D-220 Command List-V1.1.docx', 'desktop.ini']:

                    os.remove(downloads_path+'//' + file)

        return render_template('redirect.html')

    except Exception as e:

        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/image_upload', methods=['POST'])
def up_load_image():
    '''handle image,return a result page'''

    clean_temp()

    try:

        files = request.files.getlist('image')
        fail = []
        urls = []

        for image in files:

            '''grab single image and save to temp file'''
            image.save(''.join(['./temp/', image.filename]))

            '''check size'''
            if os.path.getsize(''.join(['./temp/', image.filename])) < 20*1024*1024:

                response = file_upload(''.join(['./temp/', image.filename]))

                '''check upload status code'''
                if response['code'] != 0:

                    '''fail log'''
                    fail.append(image.filename)

                else:

                    '''success log'''
                    urls.append(response['data']['image_url'])

            else:

                '''don't upload large image, return error page'''
                return 'Image: \"%s\" is too large, select images that are smaller than 20 mb' % image.filename

        if len(fail) != 0:

            '''return result with fail'''
            return 'failed to upload:\n'+str(fail)+'\n'+result_page1+(','.join(urls))+result_page2

        else:

            '''return no fail result'''
            return result_page1+(','.join(urls))+result_page2

    except Exception as e:
        '''error and error log'''

        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/video_upload', methods=['POST'])
def up_load_video():
    '''handle video, return a result page'''
    '''pretty much the same except file spliting'''

    clean_temp()

    try:

        files = request.files.getlist('video')
        urls = []
        fail = []

        for video in files:

            video.save(''.join(['./temp/', video.filename]))
            if os.path.getsize(''.join(['./temp/', video.filename])) < 15*1024*1024:

                response = file_upload(''.join(['./temp/', video.filename]))

                if response['code'] != 0:
                    fail.append(video.filename)

                else:

                    urls.append(response['data']['image_url'])

            else:

                video_slices = file_slices(
                    ''.join(['./temp/', video.filename]))

                for single_video in video_slices:
                    response = file_upload(single_video)

                    if response['code'] != 0:
                        fail.append(video.filename)

                    else:

                        urls.append(response['data']['image_url'])

        if len(fail) != 0:

            return 'failed to upload:\n'+str(fail)+'\n'+result_page1+(','.join(urls))+result_page2

        else:

            return result_page1+(','.join(urls))+result_page2

    except Exception as e:
        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/file_upload', methods=['POST'])
def upload_file():
    '''handle other files'''
    '''pretty much the same as video'''

    clean_temp()

    try:
        files = request.files.getlist('file')
        urls = []
        fail = []

        for file in files:
            file.save('./temp/%s' % file.filename)

            if os.path.getsize(''.join(['./temp/', file.filename])) < 15*1024*1024:

                response = file_upload(''.join(['./temp/', file.filename]))

                if response['code'] != 0:

                    fail.append(file.filename)

                else:

                    urls.append(response['data']['image_url'])

            else:

                video_slices = file_slices(''.join(['./temp/', file.filename]))

                for single_video in video_slices:
                    response = file_upload(single_video)

                    if response['code'] != 0:

                        fail.append(file.filename)

                    else:

                        urls.append(response['data']['image_url'])

        if len(fail) != 0:

            return 'failed to upload:\n'+str(fail)+'\n'+result_page1+(','.join(urls))+result_page2

        else:

            return result_page1+(','.join(urls))+result_page2

    except Exception as e:

        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/image_url', methods=['POST'])
def download_image():

    clean_temp()

    try:
        '''sometime the MOTHERFUCKER database absort the connection, other time some stupid system add more lines when copy'''

        urls = request.form['text']

        '''get rid of \n and \r'''
        if'\n' in urls:
            urls = urls[0:-2]

        urls = urls.split(',')
        images = ''

        for url in urls:

            '''fetch one image, and create map'''
            image = image_download(url)
            pixel = image.load()
            temp = []

            '''get original image from map'''
            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    temp.append(pixel[x, y])

            '''add original image to HTML'''
            b64 = str(base64.b64encode(bytes(temp)))[2:-1]
            images += '''<img src='data:image/png;base64,%s'><br>''' % b64

        return image_download_page % images

    except Exception as e:

        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/video_url', methods=['POST'])
def download_video():
    '''download video'''

    clean_temp()

    try:
        urls = request.form['text']
        if'\n' in urls:
            urls = urls[0:-2]
        urls = urls.split(',')
        temp = []

        for url in urls:
            '''download image and get data from its map'''
            image = image_download(url)
            pixel = image.load()

            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    temp.append(pixel[x, y])

        raw_bytes = bytes(temp)

        '''save to temp folder and return a HTML pointing it'''
        with open('./temp/temp.mp4', 'wb')as file:
            file.write(raw_bytes)

        return render_template('video.html')

    except Exception as e:

        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/file_url', methods=['POST'])
def download_file():
    '''download file'''
    '''pretty much the save, download a file instead'''

    clean_temp()

    try:

        urls = request.form['text']
        if'\n' in urls:
            urls = urls[0:-2]
        urls = urls.split(',')
        temp = []

        for url in urls:
            image = image_download(url)
            pixel = image.load()

            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    temp.append(pixel[x, y])

            raw_bytes = bytes(temp)

        with open('./temp/temp.file', 'wb')as file:
            file.write(raw_bytes)

        '''return a file to download'''
        return send_file('./temp/temp.file', as_attachment=True)

    except Exception as e:

        with open('exception.txt', 'a')as except_log:
            except_log.write(str(e))

        return 'Server error, I am sorry, I will look into it later'


@app.route('/transcendence', methods=['GET'])
def trans():
    '''in progress'''
    print('success')
    return 'recieved'


@app.route('/joke', methods=['GET'])
def joke():
    '''easter egg'''
    return redirect('https://www.bilibili.com/video/BV1PN411X7QW'), 301


# @app.errorhandler(Exception)
# def http_error_handler(error):
#     '''redirect when facing error'''
#     return redirect('https://www.youtube.com/watch?v=oxKa7J9CRNM'), 301


print()
print('Author:DAF201')
print('To support author, give a like to any video of \nhttps://www.youtube.com/channel/UCrrNHoXQ1uTYsR6v41pDalQ \n\tor \nhttps://space.bilibili.com/351609538/\nthank you\n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4123)
