import json
import uuid
from datetime import datetime

import numpy as np
import pandas as pd


def generate_uuid():
    try:
        md5 = uuid.uuid4()
        return str(md5).upper().replace('-', '')
    except Exception as e:
        print('generate_uuid error:', e)
        return None


def get_time():
    # 2022-03-03 16:12:30
    return datetime.now().strftime("%Y-%m-%d %X")


def read_excel(path, sheet_index=0, is_value=True):
    df = pd.read_excel(path, sheet_name=sheet_index)
    # nan替换为空字符串
    df1 = df.replace(np.nan, '', regex=True)
    if is_value:
        return df1.values
    else:
        return df1


def write_excel(path, result_list=[], columns=[], df=None, sheet_index=0):
    if df is None:
        df = pd.DataFrame(result_list, columns=columns)
    df.to_excel(path, index=sheet_index)


def df_to_sql(path_df, table, engine, is_df=False):
    """
    df import to sql
    :param path_df:
    :param table: sql table
    :param engine: sqlalchemy engine
    :param is_df: True为DataFrame，False为Excel路径
    :return:
    """
    # pandas批量导入mysql
    if is_df:
        df = path_df
    else:
        df = read_excel(path_df, is_value=False)
    df.to_sql(table, engine, if_exists='append', index=False)


def read_txt(path):
    data_list = []
    with open(path, encoding='utf8') as f:
        for line in f:
            data_list.append(line.strip())
    return data_list


def dump_json(obj, path):
    json.dump(obj, open(path, 'w', encoding='utf8'), ensure_ascii=False)


def load_json(path):
    return json.load(open(path, encoding='utf8'))
