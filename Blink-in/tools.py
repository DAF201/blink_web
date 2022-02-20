from glob import glob
import os
import zipfile
from PIL import Image
import numpy
import requests
from config import *

temp = './temporary/'
cover = './static/cover.gif'


def clear_temp():
    try:
        for x in glob('./temporary/*'):
            os.remove(x)
    except:
        pass


def clear_output():
    try:
        for x in glob('./output/*'):
            os.remove(x)
    except:
        pass


def factors(num):
    def is_prime(x):
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


def trans(file: str):

    if (zipfile.is_zipfile(temp+file)) and (os.path.basename(temp+file).split('.')[1] == 'gif'):
        with zipfile.ZipFile(temp+file, 'r')as zip:
            zip.extractall('./output/')
        return False
    else:
        with zipfile.ZipFile(temp+'temp.zip', 'w')as zip:
            zip.write(temp+file, os.path.basename(temp+file))
        with open(temp+'output.gif', 'wb')as output:
            with open(temp+'temp.zip', 'rb')as zip:
                with open(cover, 'rb')as output_cover:
                    output.write(output_cover.read()+zip.read())
        return True


def blink_image_process(image):
    cover_1 = Image.open(first_cover)
    cover_2 = Image.open(second_cover)
    this_img = Image.open('./temporary/'+image)
    this_size = this_img.size

    if this_img.mode == "RGBA":

        cover_1 = cover_1.resize(this_size)
        cover_2 = cover_2.resize(this_size)

        blank = Image.new("RGB", this_size, (255, 255, 255))
        blank.paste(this_img, mask=this_img.split()[3])

        this_img = numpy.array(blank)
        cover_1 = numpy.array(cover_1)
        cover_2 = numpy.array(cover_2)

        output_array = numpy.add(this_img, cover_1)
        output_array = numpy.add(output_array, cover_2)

        output = Image.fromarray(output_array)
        output.save('./output/'+image.split('.')[0]+'.png')

    else:

        cover_1 = cover_1.resize(this_size)
        cover_2 = cover_2.resize(this_size)

        this_img = numpy.array(this_img)
        cover_1 = numpy.array(cover_1)
        cover_2 = numpy.array(cover_2)

        output_array = numpy.add(this_img, cover_1)
        output_array = numpy.add(output_array, cover_2)

        output = Image.fromarray(output_array)
        output.save('./output/'+image.split('.')[0]+'.png')


def image_upload(image):
    image = open(image, 'rb')
    response = requests.post(url=data_base, headers=header, params=param, cookies=cookie, files={
                             'file_up': image, 'category': 'daily'}).text
    image.close()
    return response


def url_image_process(image):
    cover_1 = Image.open(first_cover)
    cover_2 = Image.open(second_cover)

    this_image = Image.open(image)
    this_size = this_image.size

    cover_1 = cover_1.resize(this_size)
    cover_2 = cover_2.resize(this_size)

    this_image = numpy.array(this_image)
    cover_1 = numpy.array(cover_1)
    cover_2 = numpy.array(cover_2)

    this_image = numpy.subtract(this_image, cover_1)
    this_image = numpy.subtract(this_image, cover_2)
    this_image = Image.fromarray(this_image)

    this_image.save('./output/'+os.path.basename(image))
