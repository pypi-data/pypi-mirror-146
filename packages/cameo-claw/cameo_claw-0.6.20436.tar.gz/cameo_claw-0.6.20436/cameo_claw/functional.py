from multiprocessing.dummy import Pool
from tqdm import tqdm
import cameo_claw.istarmap

cameo_claw.istarmap.ignore_no_use_warning()


def it_mp_f(f, tup_param):
    # 2022-04-10 bowen
    # fastapi + multiprocessing can crash, please use spawn to prevent it
    # https://miketarpey.medium.com/troubleshooting-usage-of-pythons-multiprocessing-module-in-a-fastapi-app-f1c368673686
    # also fail
    # finally we use: from multiprocessing.dummy import Pool
    int_progress = 0
    with Pool(200) as p:
        for result in tqdm(p.istarmap(f, tup_param), total=len(tup_param)):
            int_progress += 1
            yield int_progress, result
