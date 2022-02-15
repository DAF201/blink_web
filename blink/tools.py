from glob import glob
import os
import requests
from PIL import Image
from data import *
import json
import string
import random
import zipfile
import numpy


def random_gen(size=6, chars=string.ascii_uppercase + string.digits):
    '''generate a random name for file'''

    return ''.join(random.choice(chars) for _ in range(size))


def factors(num):
    '''find two closest factors of a number'''

    def is_prime(x):
        '''if the number is prime'''
        if (x == 2) or (x == 3):

            return True

        if (x % 6 != 1) and (x % 6 != 5):

            return False

        for i in range(5, int(x ** 0.5) + 1, 6):

            if (x % i == 0) or (x % (i + 2) == 0):

                return False

        return True

    if is_prime(num):

        return(1, num)

    else:

        start = int(pow(num, 0.5))

        if start < num-start:

            while((num % start != 0)):
                start -= 1

            return ((start, int(num/start)))

        else:

            while(num % start != 0):
                start += 1

            return (start, int(num/start))


def clear_temp():
    '''clean up temp folder for use'''
    try:

        for x in glob('./temp/*.*'):
            os.remove(x)

    except:

        pass


def image_download(url):
    '''download image from url'''

    img = Image.open(requests.get(url, stream=True).raw)

    return img


def file_slices(file):
    '''cut file into slices'''

    def cut(data, size):

        return [data[i:i+size]for i in range(0, len(data), size)]

    with open(file, 'rb')as original_file:
        original_data = list(original_file.read())

    slice_size = 6000000*2
    slices = cut(original_data, slice_size)
    output_list = []

    for x in slices:
        name = './temp/%s.png' % random_gen()
        with open(name, 'wb')as output_file:
            output_file.write(bytes(x))
        output_list.append(name)

    return output_list


def file_upload(file: str):
    '''upload file'''

    with open(file, 'rb')as file_to_be_upload:
        data = file_to_be_upload.read()

    data = list(data)
    size = factors(len(data))
    data = iter(data)
    image = Image.new('L', size, (255))
    pixel = image.load()

    for x in range(size[0]):
        for y in range(size[1]):
            pixel[x, y] = next(data)

    if file.endswith('png') == False:
        file += '.png'

    image.save(file)

    response = requests.post(url=data_base, headers=header, params=param, cookies=cookie, files={
                             'file_up': open(file, 'rb'), 'category': 'daily'}).text

    response = json.loads(response)

    return response


def transcendence(file):
    '''make file to gif'''

    files = glob('./trans_temp/*.*')

    for single_file in files:
        os.remove(single_file)

    if zipfile.is_zipfile(file):

        with zipfile.ZipFile(file, 'r')as zip:
            zip.extractall('./trans_temp')

        os.remove(file)

        last_file = max(glob('./trans_temp/*.*'), key=os.path.getctime)

        name = os.path.basename(last_file)

        file_array = numpy.load(last_file)

        file_array.tofile('./temp/'+name)

        return True

    else:

        file_name = os.path.basename(file).split('.')[0]
        file_ext = os.path.basename(file).split('.')[1]

        numpy.save('./trans_temp/'+file_name, numpy.fromfile(file))

        os.rename('./trans_temp/'+file_name+'.npy',
                  './trans_temp/'+file_name+'.'+file_ext)

        with zipfile.ZipFile('./trans_temp/temp.zip', 'w')as zip:
            zip.write('./trans_temp/'+file_name+'.'+file_ext,
                      os.path.basename('./trans_temp/'+file_name+'.'+file_ext))

        with open('./trans_temp/temp.gif', 'wb')as out:
            with open('./config/cover.gif', 'rb')as cover:
                with open('./trans_temp/temp.zip', 'rb')as file:
                    out.write(cover.read()+file.read())

        for x in glob('./trans_temp/*.*'):
            if x != r'./trans_temp\temp.gif':
                os.remove(x)

        return False
