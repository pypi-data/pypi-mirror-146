from multiprocessing import Pool
import multiprocessing
from tqdm import tqdm
import cameo_claw.istarmap

cameo_claw.istarmap.ignore_no_use_warning()


def it_mp_f(f, tup_param):
    # fastapi + multiprocessing can crash, please use spawn to prevent it
    # https://miketarpey.medium.com/troubleshooting-usage-of-pythons-multiprocessing-module-in-a-fastapi-app-f1c368673686
    multiprocessing.set_start_method('spawn')
    int_progress = 0
    with Pool(25) as p:
        for result in tqdm(p.istarmap(f, tup_param), total=len(tup_param)):
            int_progress += 1
            yield int_progress, result
