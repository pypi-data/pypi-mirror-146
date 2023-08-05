import requests

from cameo_claw.file import mkdir


def requests_get(f, url, target_directory):
    print('201')
    mkdir(target_directory)
    print('202', url)
    r = requests.get(url, stream=True)
    print('203')
    if r.status_code == 200:
        print('204')
        bytes1 = r.raw.read()
        print('205')
        if len(bytes1) > 180:  # size larger than 180 bytes we assume the file is not empty
            print('206')
            return f(bytes1)
