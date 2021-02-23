from datetime import datetime
from pykrx import stock
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
import os, glob
from datetime import datetime
import numpy as np
Krx_Char_folder_path = 'E:/Krx_Chart_folder'
condition = '.csv'

def pykrx_scratch(date_Start, date_End):
    print("Reading Daily Chart ... {} - {}".format(date_Start, date_End))
    # create main folder
    if not os.path.exists(Krx_Char_folder_path):
        os.mkdir(Krx_Char_folder_path)
    # ticker scratch
    for ticker in stock.get_market_ticker_list(market="ALL"):
        stock_name = stock.get_market_ticker_name(ticker)
        stock_folder_name = stock_name + '_' + ticker
        #print(stock_name, ticker)
        df = stock.get_market_ohlcv_by_date(date_Start, date_End, ticker)
        df = df.reset_index()
        #print(len(df))
        df.insert(5, '수정종가', df['종가'])
        # folder check
        if not os.path.exists(Krx_Char_folder_path + '/' + stock_name):
            os.mkdir(Krx_Char_folder_path + '/' + stock_name)
        df.to_csv(Krx_Char_folder_path + '/' + stock_name + '/' + ticker + '.csv', sep=',', na_rep='0', index=False, header=False)
        print('{} Daily chart is written! ==== ticker is : {}'.format(stock_name, ticker))
    print('Scratching daily chart is done!')

def pykrx_daily_update():
    #today_date = datetime.today().strftime("%Y%m%d")
    today_date = '20210223'
    df = stock.get_market_ohlcv_by_ticker(today_date, market="ALL")
    df = df.reset_index()
    del df['거래대금']
    del df['등락률']
    df_format = df
    df.insert(5, '수정종가', df['종가'])
    count = 0
    for ticker in df['티커']:
        stock_name = stock.get_market_ticker_name(ticker)
        ticker_csv = pykrx_read_csv(stock_name)
        df_list = list(np.array(df.iloc[i].tolist()))
        df_list[0] = datetime.today().strftime("%Y-%m-%d")
        df_save = ticker_csv.append(pd.Series(df_list, index=ticker_csv.columns), ignore_index=True)
        count += 1

def search(data_path, extension):
    """Returns the list of files have extension (only current directory)
    Args:
        data_path (str): data path
        extension (str): extension
    Returns:
        file_list (list): file list with path
   """
    file_list = []
    for filename in os.listdir(data_path):
        ext = os.path.splitext(filename)[-1]
        if ext == extension:
            file_list.append(data_path+'/'+filename)
    return file_list

def pykrx_read_csv(stock_name):
    csv_file_path = search(Krx_Char_folder_path + '/' + stock_name, condition)
    if os.path.exists(csv_file_path[0]):
        stock_csv = pd.read_csv(csv_file_path[0])
    else:
        print('Can''t find csv file!')
    return stock_csv
    print('read done!')

def pykrx_read_train_set():

    # print(df.iloc[:, 4:5].tail())
    # minmax = MinMaxScaler().fit(df.iloc[:, 4:5].astype('float32'))  # Close index
    # df_log = minmax.transform(df.iloc[:, 4:5].astype('float32'))  # Close index
    # df_log = pd.DataFrame(df_log)
    # df_log.head()
    # df_train = df_log
    # df.shape, df_train.shape
    print('read done!')
