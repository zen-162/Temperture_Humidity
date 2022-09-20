# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import urllib.request
from bs4 import BeautifulSoup

import datetime
import csv
import os
from decimal import ROUND_HALF_UP, Decimal

#csv_file
csv_file_name = '//home/zen/Documents/Geek/Test_TemperatureHumidity/test_data1.csv'
api_csv_file_name = '/home/zen/Documents/Geek/Test_TemperatureHumidity/test_data_JMA.csv'

# CSV の列
fields = ['date', 'time', 'temperature', 'humidity', 'absolute_humidity']

start_times=0 #from 0 min
get_times=20 #every 20 min


def str2float(weather_data):
    try:
        return float(weather_data)
    except:
        return 0

def scraping(url, date):

    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('table', { 'class' : 'data2_s' })

    data_list = []
    data_list_per_hour = []

    # table の中身を取得
    for tr in trs.findAll('tr')[2:]:
        tds = tr.findAll('td')

        if tds[1].string == None:
            break

        data_list.append(format(date, '%Y/%m/%d'))
        data_list.append(tds[0].string) # 時
        data_list.append(str2float(tds[4].string)) # 気温(℃)
        data_list.append(str2float(tds[7].string)) # 湿度(%)

        absthumi = 217*(6.1078*10**(7.5*data_list[2]/(data_list[2]+237.3)))/(data_list[2]+273.15)*data_list[3]/100
        a_absthumi = Decimal(str(absthumi))
        str_absolute_humi = a_absthumi.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        absthumi = float(str_absolute_humi)
        data_list.append(absthumi) # 絶対湿度

        data_list_per_hour.append(data_list)

        data_list = []

    return data_list_per_hour

def create_csv(datas):
    with open(csv_file_name, 'a') as input_f:
        writer = csv.writer(input_f, lineterminator='\n')

        if os.stat(csv_file_name).st_size == 0:
            writer.writerow(fields)

        df = pd.read_csv(csv_file_name, header=0, names=fields)

        if(len(df) == 0): #headerのみの場合
            writer.writerow(datas)

        else:
            tail_data = df.tail(1)
            pre_datas = np.array(tail_data)
            # 例）pre_datas = [['2022/09/05' '16時20分33秒' 27 70]] 前回の取得したデータ
            # 例）datas = ['2022/09/05', '16時22分44秒', 27, 70]

            pre_str = pre_datas[0][0] + ' ' + pre_datas[0][1]
            str = datas[0] + ' ' + datas[1]

            #print('str: ', str)

            pre_tdatetime = datetime.datetime.strptime(pre_str, '%Y/%m/%d %H:%M:%S')
            tdatetime = datetime.datetime.strptime(str, '%Y/%m/%d %H:%M:%S')
            #time = datetime.datetime(time)
            #print('tdatetime: ', tdatetime)

            #csvファイルへの書き込み
            #if (tdatetime)
            if pre_tdatetime.day != tdatetime.day:
                writer.writerow('')
            writer.writerow(datas)

            # 毎日1時頃に更新されるデータなので、7時に取得
            if((tdatetime.hour == 7) and (start_times <= tdatetime.minute < start_times+get_times)):
                # データ取得開始・終了日 例）datas[0] = 2022/08/31
                year = tdatetime.year
                month = tdatetime.month
                day = tdatetime.day
                start_date = datetime.date(year, month, day)

                #with open(csv_file_name, 'w') as f:
                with open(api_csv_file_name, 'a') as output_f:
                    writer = csv.writer(output_f, lineterminator='\n')
                    writer.writerow('')

                    # 気象庁のデータのheader
                    if os.stat(api_csv_file_name).st_size == 0:
                        writer.writerow(fields)

                    date = start_date - datetime.timedelta(days=1)
                    #print('date', date)
                    #while date != end_date + datetime.timedelta(1):

                    # 対象url（会津）
                    url = 'http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?' \
                            'prec_no=36&block_no=47570&year=%d&month=%d&day=%d&view='%(date.year, date.month, date.day)
                            #https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=36&block_no=47570&year=2022&month=8&day=29&view=p1
                            #https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=36&block_no=47570&year=2022&month=8&day=29&view=p1

                    data_per_day = scraping(url, date)

                    for dpd in data_per_day:
                        writer.writerow(dpd)

                    #date += datetime.timedelta(1)

            # for data in datas:
            #     writer.writerow(data)
