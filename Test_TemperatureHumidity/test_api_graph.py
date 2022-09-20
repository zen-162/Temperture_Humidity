#import pandas as pd
#import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import os

#from matplotlib.dates import DateFormatter
#from matplotlib.dates import date2num
import matplotlib.ticker as ticker

csv_file_name = '/home/zen/Documents/Geek/Test_TemperatureHumidity/test_tepm_humi_api.csv'
image_file_path = '/home/zen/Documents/Geek/Test_TemperatureHumidity/data_api_image'
image_file_name = ['api_temperature.png', 'api_humidity.png', 'api_absolute_humidity.png']

data_num = 5 # データの数
graph_num = 3 # 気温, 湿度, 絶対湿度, 気象庁

# フォント設定
#plt.rcParams['font.family'] = 'IPAexGothic'

# csv読み取りグラフように値を変換
def create_data():
    newline_num = 0 # 改行の数
    rows = []
    data = []
    ttime_array = []
    t = [] #追加！
    i_zero_flag = False # csvファイルのheader以外の先頭が空白の場合

    start_day = ''
    end_day = ''

    with open(csv_file_name) as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    header = rows.pop(0)

    for i in range(len(rows)):
        if rows[i] == []:
            # if i == 0:
            #     i_zero_flag = True
            newline_num = newline_num + 1
            continue

        data = np.append(data, rows[i])

        #print('data: ', data)

        if data[(i-newline_num)*data_num+1] == '24':
            data[(i-newline_num)*data_num+1] = '00'
        str_datetime = data[(i-newline_num)*data_num] + ' ' + data[(i-newline_num)*data_num+1]+':00:00'

        #日付時間型で扱う
        tdatetime = datetime.datetime.strptime(str_datetime, '%Y/%m/%d %H:%M:%S')

        #t = np.append(t, datetime.time(tdatetime.hour, tdatetime.minute))
        #print('t: ', t)

        # タイトルの日付
        tdate = str(tdatetime.month) + '/' + str(tdatetime.day)
        if start_day == '':
            start_day = tdate
            end_day = start_day
        elif end_day != tdate:
            end_day = tdate

        ttime = str(tdatetime.hour) # + ':' +  str(tdatetime.minute)
        ttime_array = np.append(ttime_array, ttime)

    #if i_zero_flag == True:
    data = data.reshape((i-(newline_num)+1), data_num)
    #else:
        #data = data.reshape((i-(newline_num)+1), data_num)

    data = data.transpose() # 転置
    #ew_t = date2num(t)

    return ttime_array, data, header, start_day, end_day


# グラフを作成
def create_graph():
    x_data, y_data, title, start_day, end_day = create_data()

    fig = plt.figure(dpi=170)
    for j in range(graph_num):
        num = j + 1
        #ax = fig.add_subplot(graph_num, 1, num)
        ax = fig.add_subplot(1, 1, 1)

        # ax.set_major_locator(ticker.FixedLocator(x_data))
        # ax.set_major_formatter(DateFormatter('%H:%M'))
        #ax.tick_params(axis='x', rotation=270)

        graph_data = np.asfarray(y_data[num+1], dtype=float) #気温:2, 湿度:3, 絶対湿度:4
        #plt.xlabel(title[1])
        plt.xlabel('hour:minute')
        plt.xticks(rotation=270, fontsize=7)
        plt.ylabel(title[num+1])
        plt.plot(x_data, graph_data, label=title[num+1], linestyle='solid', marker='o')

        plt.ylim([min(plt.ylim())-0.5, max(plt.ylim())+0.5])
        plt.title(f'{start_day}~{end_day} {title[num+1]}')
        plt.legend(loc='upper right')
        plt.minorticks_on()

        plt.tight_layout()
        plt.savefig(os.path.join(image_file_path, image_file_name[j]))
        plt.close('all')

if __name__ == '__main__':
    create_graph()
