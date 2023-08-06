import requests

from cameo_claw.file import mkdir
import os


def url_to_filename(url, is_ext=False):
    filename = os.path.basename(url)
    if not is_ext:
        filename = filename[:filename.find('.')]
    return filename


def requests_get(f, url, target_directory, is_cache=True):
    pass


#     filename = url_to_filename(url, is_ext=True)
#     directory = './data/cache/'
#     mkdir(directory)
#     path = directory + filename
#     if is_cache and os.path.isfile(path):
#         with open(path, 'rb') as file:
#             print('hit disk cache:', path)
#             return f(file.read())
#     mkdir(target_directory)
#     r = requests.get(url, stream=False)
#     if r.status_code == 200:
#         bytes1 = r.raw.read()
#         if len(bytes1) > 180:  # size larger than 180 bytes we assume the file is not empty
#             if is_cache:
#                 with open(path, 'wb') as file:
#                     print('write disk cache:', path)
#                     file.write(bytes1)
#             return f(bytes1)


def requests_get_bytes(url):
    r = requests.get(url)
    if r.status_code == 200:
        bytes1 = r.content
        if len(bytes1) > 180:  # size larger than 180 bytes we assume the file is not empty
            return bytes1
        else:
            return b''


def requests_get_ram_cache(f, url, target_directory):
    return f(requests_get_bytes(url))
