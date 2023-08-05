import warnings
warnings.filterwarnings('ignore')
import time
from autox.autox_server.util import log

def get_origin_fe(G_hist, G_data_info):
    txt = 'SELECT '

    x1 = [list(x.keys())[0] for x in G_data_info['entities']['main']['columns']]
    x2 = G_hist['feature_selection_used_features']

    used_cols = list(set(x1) & set(x2))

    for col in used_cols:
        txt += f'{col}, '
    txt = txt[:-2]
    txt += ' FROM main_train WINDOW w1 as (PARTITION BY unique_id ORDER BY unique_id ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)'

    return txt, used_cols


def get_time_fe(G_hist):
    def filter_time_feature(col_name):
        for suffix in ['year', 'month', 'day', 'hour', 'weekofyear', 'dayofweek']:
            if col_name.endswith('_' + suffix):
                return True
        return False

    used_cols = []

    txt = 'SELECT '
    for col in G_hist['preprocess']['parsing_time']['main']:
        col_features = [x for x in G_hist['feature_selection_used_features'] if
                        (col + '_') in x and filter_time_feature(x)]
        for col_feature in col_features:
            if col_feature.endswith('_' + 'year'):
                txt += f'year({col}) as {col}_year, '
                used_cols.append(f'{col}_year')
            elif col_feature.endswith('_' + 'month'):
                txt += f'month({col}) as {col}_month, '
                used_cols.append(f'{col}_month')
            elif col_feature.endswith('_' + 'day'):
                txt += f'day({col}) as {col}_day, '
                used_cols.append(f'{col}_day')
            elif col_feature.endswith('_' + 'hour'):
                txt += f'hour({col}) as {col}_hour, '
                used_cols.append(f'{col}_hour')
            elif col_feature.endswith('_' + 'weekofyear'):
                txt += f'weekofyear({col}) as {col}_weekofyear, '
                used_cols.append(f'{col}_weekofyear')
            elif col_feature.endswith('_' + 'dayofweek'):
                txt += f'dayofweek({col}) as {col}_dayofweek, '
                used_cols.append(f'{col}_dayofweek')
    txt = txt[:-2]
    txt += ' FROM main_train WINDOW w1 as (PARTITION BY unique_id ORDER BY unique_id ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)'

    return txt, used_cols


def merge_sql(G_hist, G_data_info):
    sql_1, used_cols_1 = get_origin_fe(G_hist, G_data_info)
    sql_2, used_cols_2 = get_time_fe(G_hist)

    sql_1 = sql_1.replace('SELECT ', 'SELECT unique_id as unique_id1, ')
    sql_2 = sql_2.replace('SELECT ', 'SELECT unique_id as unique_id2, ')

    final_used_cols = used_cols_1 + used_cols_2
    fina_sql = f'''select {', '.join(final_used_cols)} FROM
    ({sql_1}) as out1 last join 
    ({sql_2}) as out2 on out1.unique_id1 = out2.unique_id2'''

    return fina_sql, final_used_cols

def create_table_sql(G_data_info):
    type_map = {
        'Str': 'string',
        'DateTime': 'date',
        'Num': 'double',
    }
    col_type_txt = ''
    for item in G_data_info['entities']['main']['columns']:
        col = list(item.keys())[0]
        col_type = type_map[list(item.values())[0]]
        col_type_txt += f'{col} {col_type}, '
    col_type_txt += 'unique_id bigint'
    sql = f'CREATE TABLE main_train({col_type_txt});'
    return sql


def get_load_sql(path_output):
    sql = f'''LOAD DATA INFILE '{path_output}/main_train_sep_t.csv' INTO TABLE main_train options(format='csv', header=true, delimiter='\t', null_value='');
    '''
    return sql


def get_sql(G_df_dict, G_data_info, G_hist, is_train, path_output, remain_time):

    start = time.time()
    log('[+] get openmldb sql')

    if is_train:
        select_sql, final_used_cols = merge_sql(G_hist, G_data_info)
        G_hist['final_sql'] = select_sql
        G_hist['sql_final_used_cols'] = final_used_cols
        G_hist['create_sql'] = create_table_sql(G_data_info)
        G_hist['load_sql'] = get_load_sql(path_output)

    end = time.time()
    remain_time -= (end - start)
    log("time consumption: {}".format(str(end - start)))
    log("remain_time: {} s".format(remain_time))
    return remain_time

