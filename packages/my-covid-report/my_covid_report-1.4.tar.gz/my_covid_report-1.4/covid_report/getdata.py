# data processing
import pandas as pd
import numpy as np
from datetime import timedelta, datetime


# data visualization
import plotly.graph_objs as go
from plotly.graph_objs import Bar, Layout
from plotly import offline
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

# change text color
import colorama
from colorama import Fore, Style

def GET_csse_covid_19_time_series():


    print('正在读取【时间序列】数据......')
    repo = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

    ts_confirmed_us = pd.read_csv(repo+'time_series_covid19_confirmed_US.csv')
    ts_confirmed_global = pd.read_csv(repo+'time_series_covid19_confirmed_global.csv')

    ts_deaths_us = pd.read_csv(repo+'time_series_covid19_deaths_US.csv')
    ts_deaths_global = pd.read_csv(repo+'time_series_covid19_deaths_global.csv')

    ts_recovered_global = pd.read_csv(repo+'time_series_covid19_recovered_global.csv')


    print('读取完毕')
    return ts_confirmed_us,ts_confirmed_global,ts_deaths_us,ts_deaths_global,ts_recovered_global



def GET_csse_covid_19_daily_reports():

    print('正在读取【横截面】数据......')

    # global
    ts_confirmed_us = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

    latest = pd.to_datetime(ts_confirmed_us.columns[-1]).strftime('%m-%d-%Y')
    prev = (pd.to_datetime(ts_confirmed_us.columns[-1])+timedelta(-1)).strftime('%m-%d-%Y')

    url_latest_global = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{latest}.csv'
    latest_data_global = pd.read_csv(url_latest_global)

    url_prev_global = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{prev}.csv'
    prev_data_global = pd.read_csv(url_prev_global)

    url_latest_us = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{latest}.csv'
    latest_data_us = pd.read_csv(url_latest_us)

    url_prev_us = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{prev}.csv'
    prev_data_us = pd.read_csv(url_prev_us)


    print('读取完毕')
    return latest_data_global,prev_data_global,latest_data_us,prev_data_us

def GET_shanghai_data(plot = False):
    print('正在获取并处理【上海】数据（数据来自上海卫健委）......')
    data = pd.read_csv('https://gitee.com/gzjzg/whale-pkg/raw/master/covid.csv')['detail']
    c = 0
    for i in data:
        if i.startswith('上海'):
            c += 1
    df = []
    for s in data.sort_values()[-c:]:
        loc = s[:2]
        date = s.split("，")[0][2:]
        in_incre = s.split(" ")[0].split('例')[1]
        in_asymptomatic = s.split(" ")[1].split('例')[0][10:]


        col_dict = {'位置':loc,'日期':date,'本土新增':in_incre,
                    '本土无症状':in_asymptomatic}
        df.append(col_dict)
    df = pd.DataFrame(df, columns=list(col_dict.keys()))

    from datetime import datetime
    df['日期']= pd.to_datetime([datetime.strptime(x,'%Y年%m月%d日') for x in df['日期']])
    df.iloc[:,2:] = df.iloc[:,2:].astype('int32')
    df = df.set_index('日期').drop('位置',axis=1)
    df = df.sort_index()

    if plot:
        fig, axes = plt.subplots(nrows=2, ncols=1,figsize = [10,5*2])

        for col,ax in zip(df.columns,axes):
            ax.plot(df.index, df[col], 'r.-')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'{col.upper()}')

        plt.tight_layout()
    return df