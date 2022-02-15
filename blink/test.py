import zipfile
import numpy
from glob import glob
import os


def transcendence(file):
    '''make file to gif'''

    files = glob('./trans_temp/*.*')

    for single_file in files:
        os.remove(single_file)

    if zipfile.is_zipfile(file):

        with zipfile.ZipFile(file, 'r')as zip:
            zip.extractall('./trans_temp')

        last_file = max(glob('./trans_temp/*.*'), key=os.path.getctime)
        
        name = os.path.basename(last_file)

        file_array = numpy.load(last_file)

        os.remove(last_file)

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


transcendence('fzzl.png')
