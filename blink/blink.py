from Flask import request, render_template, Flask, send_file
import os
import base64
from data import *
from tools import *


app = Flask(__name__, static_folder='./temp',
            template_folder='./templates')


@app.route('/')
def home():
    '''Home page'''

    return home_page


@app.route('/image_upload', methods=['POST'])
def up_load_image() -> str:
    '''handle image,return a result page'''

    try:
        clean_temp()
    except:
        pass

    try:

        files = request.files.getlist('image')

        urls = []

        for image in files:
            image.save(''.join(['./temp/', image.filename]))
            if os.path.getsize(''.join(['./temp/', image.filename])) < 20*1024*1024:

                response = file_upload(''.join(['./temp/', image.filename]))

                if response['code'] != 0:

                    return 'the far end rejected some/all of the requests'

                else:

                    urls.append(response['data']['image_url'])

            else:

                return "Image: %s is too large, select images that are smaller than 20 mb" % image

        return result_page1+(','.join(urls))+result_page2

    except Exception as e:

        return e


@app.route('/video_upload', methods=['POST'])
def up_load_video():
    '''handle video, return a result page'''

    try:
        clean_temp()
    except:
        pass

    try:

        files = request.files.getlist('video')
        urls = []

        for video in files:

            video.save(''.join(['./temp/', video.filename]))
            if os.path.getsize(''.join(['./temp/', video.filename])) < 15*1024*1024:

                response = file_upload(''.join(['./temp/', video.filename]))

                if response['code'] != 0:

                    return 'the far end rejected some/all of the requests'

                else:

                    urls.append(response['data']['image_url'])

            else:

                video_slices = file_slices(
                    ''.join(['./temp/', video.filename]))

                for single_video in video_slices:
                    response = file_upload(single_video)

                    if response['code'] != 0:

                        return 'the far end rejected some/all of the requests'

                    else:

                        urls.append(response['data']['image_url'])

        return result_page1+(','.join(urls))+result_page2

    except Exception as e:

        return e


@app.route('/file_upload', methods=['POST'])
def upload_file():
    '''handle other files'''

    try:
        clean_temp()
    except:
        pass

    try:
        files = request.files.getlist('file')
        urls = []

        for file in files:
            file.save('./temp/%s' % file.filename)

            if os.path.getsize(''.join(['./temp/', file.filename])) < 15*1024*1024:

                response = file_upload(''.join(['./temp/', file.filename]))

                if response['code'] != 0:

                    return 'the far end rejected some/all of the requests'

                else:

                    urls.append(response['data']['image_url'])

            else:

                video_slices = file_slices(''.join(['./temp/', file.filename]))

                for single_video in video_slices:
                    response = file_upload(single_video)

                    if response['code'] != 0:

                        return 'the far end rejected some/all of the requests'

                    else:

                        urls.append(response['data']['image_url'])

        return result_page1+(','.join(urls))+result_page2

    except Exception as e:

        return e


@app.route('/image_url', methods=['POST'])
def download_image():

    try:
        clean_temp()
    except:
        pass

    try:
        urls = request.form['text']
        if'\n' in urls:
            urls = urls[0:-2]
        urls = urls.split(',')
        images = ''
        counter = 0

        for url in urls:
            image = image_download(url)
            pixel = image.load()
            temp = []

            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    temp.append(pixel[x, y])

            b64 = str(base64.b64encode(bytes(temp)))[2:-1]
            images += '''<img src="data:image/png;base64,%s"><br>''' % b64
            counter += 1

        return image_download_page1+images+image_download_page2

    except Exception as e:

        return e


@app.route('/video_url', methods=['POST'])
def download_video():
    '''download video'''

    try:
        clean_temp()
    except:
        pass

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

        with open('./temp/temp.mp4', 'wb')as file:
            file.write(raw_bytes)

        return render_template('video.html')

    except Exception as e:

        return e


@app.route('/file_url', methods=['POST'])
def download_file():
    '''download file'''

    try:
        clean_temp()
    except:
        pass

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

        return send_file('./temp/temp.file', as_attachment=True)

    except Exception as e:

        return e


print('Author:DAF201')
print('To support author, give a like to any video of \nhttps://www.youtube.com/channel/UCrrNHoXQ1uTYsR6v41pDalQ \n\tor \nhttps://space.bilibili.com/351609538/\nthank you\n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
