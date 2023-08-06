import requests
import os


def url_to_filename(url, is_ext=False):
    filename = os.path.basename(url)
    if not is_ext:
        filename = filename[:filename.find('.')]
    return filename


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
