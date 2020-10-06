import pandas as pd
import numpy as np

def create_mapping_dict():
    de_para_colunas = pd.read_csv('../novas_colunas.txt',sep=';')
    return dict(zip(de_para_colunas['Coluna_original'].tolist(),de_para_colunas['Coluna_renomeada'].tolist()))

def map_to_new_columns_name(old_cols):
    map_dict = create_mapping_dict()
    new_cols = []
    for col in old_cols:
        if col in map_dict.keys(): new_cols.append(map_dict[col])
        else: new_cols.append(col)
    return new_cols