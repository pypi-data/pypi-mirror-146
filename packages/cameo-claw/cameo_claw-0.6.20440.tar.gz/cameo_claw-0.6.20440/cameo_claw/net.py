import requests

from cameo_claw.file import mkdir
import os


def url_to_filename(url, is_ext=False):
    filename = os.path.basename(url)
    if not is_ext:
        filename = filename[:filename.find('.')]
    return filename


def requests_get(f, url, target_directory):
    filename = url_to_filename(url, is_ext=True)
    directory = './data/cache/'
    mkdir(directory)
    path = directory + filename
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            return f(file.read())
    mkdir(target_directory)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        bytes1 = r.raw.read()
        if len(bytes1) > 180:  # size larger than 180 bytes we assume the file is not empty
            with open(path, 'wb') as file:
                file.write(bytes1)
            return f(bytes1)
