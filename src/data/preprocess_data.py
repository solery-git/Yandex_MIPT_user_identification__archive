# -*- coding: utf-8 -*-
import pickle
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
PATH_RAW = 'data/raw'
PATH_INTERIM = 'data/interim'
PATH_PROCESSED = 'data/processed'


def fix_incorrect_date_formats(df, columns_to_fix):
    for time_col in columns_to_fix:
        d = df[time_col]
        index_mask = (d.dt.day <= 12)
        d_fix = d[index_mask]
        d_fix = pd.to_datetime(d_fix.apply(str), format='%Y-%d-%m %H:%M:%S')
        df.loc[index_mask, time_col] = d_fix
    return df


def main():
    train_df = pd.read_csv(PROJECT_DIR.joinpath(PATH_RAW, 'train_sessions.csv'), index_col='session_id')
    test_df = pd.read_csv(PROJECT_DIR.joinpath(PATH_RAW, 'test_sessions.csv'), index_col='session_id')
    
    
    train_df = train_df.sort_values(by='time1')
    train_test_df = pd.concat([train_df, test_df], sort=False)
    sites_train_test = train_test_df[['site%d' % i for i in range(1, 11)]].fillna(0).astype('int')
    timestamps_train_test = train_test_df[['time%d' % i for i in range(1, 11)]].fillna(np.datetime64('NaT')).astype(np.datetime64)
    timestamps_train_test = fix_incorrect_date_formats(timestamps_train_test, timestamps_train_test.columns)
    y = train_df['target'].astype('int').values
    
    
    with open(PROJECT_DIR.joinpath(PATH_INTERIM, 'sites_train_test.pkl'), 'wb') as fout:
        pickle.dump(sites_train_test, fout, protocol=2)
    
    with open(PROJECT_DIR.joinpath(PATH_INTERIM, 'timestamps_train_test.pkl'), 'wb') as fout:
        pickle.dump(timestamps_train_test, fout, protocol=2)
    
    with open(PROJECT_DIR.joinpath(PATH_INTERIM, 'train_size.pkl'), 'wb') as fout:
        pickle.dump(len(train_df), fout, protocol=2)
    
    with open(PROJECT_DIR.joinpath(PATH_PROCESSED, 'y.pkl'), 'wb') as fout:
        pickle.dump(y, fout, protocol=2)
    

if __name__ == '__main__':
    main()