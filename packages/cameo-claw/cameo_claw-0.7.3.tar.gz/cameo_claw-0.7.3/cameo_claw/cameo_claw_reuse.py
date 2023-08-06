import gzip
from io import BytesIO, StringIO
import polars as pl

from cameo_claw.file import mkdir
from cameo_claw.net import url_to_filename, requests_get_ram_cache

import warnings
import pandas as pd
from cameo_claw.functional import it_mp_f

warnings.filterwarnings("ignore")


def bytesio_to_gzip(df, url, target_directory):
    bytesio, filename = bytesio_filename(df, url)
    path = f'{target_directory}{filename}.csv.gz'
    write_gzip(bytesio, path)
    return url


def requests_get_write(target_directory, url, f_write):
    try:
        return requests_get_ram_cache(f_write, url, target_directory)
    except Exception as e:
        print(f'cameo_claw.py,requests_get_write,Exception:{e, url}')


def bytesio_filename(df, url):
    bytesio = BytesIO()
    df.to_csv(bytesio)
    filename = url_to_filename(url)
    return bytesio, filename


def write_gzip(bytesio, path):
    with gzip.open(path, 'wb') as f:
        f.write(bytesio.getvalue())


def pl_read_csv_distinct(bytes1, lst_distinct_column):
    df = pl.read_csv(bytes1, infer_schema_length=20000)
    df = df.distinct(subset=lst_distinct_column)
    return df


def pl_read_csv_str(bytes1):
    return pl.read_csv(bytes1, infer_schema_length=0).with_columns(pl.all().cast(pl.Int32, strict=False))


def pd_read_csv(bytes1):
    df = None
    if bytes1[0:2] == b'\x1f\x8b':
        df = pd.read_csv(BytesIO(bytes1), compression='gzip')
    else:
        df = pd.read_csv(BytesIO(bytes1))
    return df


def groupby_write_gzip(df, url, lst_group_by_column, target_directory):
    g = df.groupby(lst_group_by_column)
    for df in g:
        filename_tail = '_group_' + '-'.join(list(
            map(lambda column:
                str(df.row(0)[df.find_idx_by_name(column)]).replace('_', '-'),
                lst_group_by_column)))
        bytesio, filename = bytesio_filename(df, url)
        path = f'{target_directory}{filename}{filename_tail}.csv.gz'
        mkdir(target_directory)
        write_gzip(bytesio, path)
    return url


def it_lst_url_f(f, lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column):
    return it_mp_f(f, [tuple([url, target_directory, lst_distinct_column,
                              lst_column_match, sort_column]) for url in lst_url])


def condition_filter_sort(df, lst_column_match, sort_column):
    condition = ''
    for lst_col_val in lst_column_match:
        condition += f"""(pl.col('{lst_col_val[0]}')=='{lst_col_val[1]}') | """
    condition = condition[:-3]
    df = df.filter(eval(condition))
    if sort_column:
        df = df.sort(sort_column)
    return df


def distinct_filter_sort(bytes1, lst_distinct_column, lst_column_match, sort_column):
    df = pl_read_csv_distinct(bytes1, lst_distinct_column)
    df = condition_filter_sort(df, lst_column_match, sort_column)
    return df
