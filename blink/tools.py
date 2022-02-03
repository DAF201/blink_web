from glob import glob
import os
import requests
from PIL import Image
from data import *
import json
import string
import random


def random_gen(size=6, chars=string.ascii_uppercase + string.digits):
    '''generate a random name for file'''

    return ''.join(random.choice(chars) for _ in range(size))


def factors(num):
    '''find two closest factors of a number'''

    def is_prime(x) -> bool:

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


def clean_temp():
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
