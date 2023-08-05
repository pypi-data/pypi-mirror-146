import gzip
import os
from io import BytesIO
import polars as pl
from cameo_claw.net import requests_get

import warnings
import pandas as pd

warnings.filterwarnings("ignore")


def bytesio_to_gzip(df, url, target_directory):
    bytesio, filename = bytesio_filename(df, url)
    path = f'{target_directory}{filename}.csv.gz'
    write_gzip(bytesio, path)
    return url


def requests_get_write(target_directory, url, f_write):
    try:
        return requests_get(f_write, url, target_directory)
    except Exception as e:
        print(f'cameo_claw.py,requests_get_write,Exception:{e, url}')


def bytesio_filename(df, url):
    bytesio = BytesIO()
    df.to_csv(bytesio)
    filename = os.path.basename(url)
    filename = filename[:filename.find('.')]
    return bytesio, filename


def write_gzip(bytesio, path):
    with gzip.open(path, 'wb') as f:
        f.write(bytesio.getvalue())


def read_csv_distinct(bytes1, lst_distinct_column):
    print('119', len(bytes1))
    print(bytes1[0:10])
    print('119.1')
    # df = pl.read_csv(bytes1, infer_schema_length=20000)
    print('119.2')
    df_pandas = pd.read_csv(bytes1)
    print('119.3')
    df = pl.from_pandas(df_pandas)
    print('119.4')
    print('120')
    df = df.distinct(subset=lst_distinct_column)
    print('121')
    return df


def read_csv_str(bytes1):
    return pl.read_csv(bytes1, infer_schema_length=0).with_columns(pl.all().cast(pl.Int32, strict=False))
