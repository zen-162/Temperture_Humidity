import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import os

#from matplotlib.dates import DateFormatter
#from matplotlib.dates import date2num
import matplotlib.ticker as ticker

csv_file_name_1 = '/home/zen/Documents/Geek/Test_TemperatureHumidity/test_data1.csv'
csv_file_name_2 = '/home/zen/Documents/Geek/Test_TemperatureHumidity/test_data2.csv'

image_file_path = '/home/zen/Documents/Geek/Test_TemperatureHumidity/data_image'
image_file_name = ['temperature.png', 'humidity.png', 'absolute_humidity.png']

data_num = 5 # データの数
graph_num = 3 # 気温, 湿度, 絶対湿度, 気象庁

# フォント設定
#plt.rcParams['font.family'] = 'IPAexGothic'

# csv読み取りグラフように値を変換
def create_data(file_name):
    newline_num = 0 # 改行の数
    rows = []
    data = []
    ttime_array = []
    t = [] #追加！
    i_zero_flag = False # csvファイルのheader以外の先頭が空白の場合

    start_day = ''
    end_day = ''

    with open(file_name) as f:
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

        str_datetime = data[(i-newline_num)*data_num] + ' ' + data[(i-newline_num)*data_num+1]


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

        ttime = str(tdatetime.hour) + ':' +  str(tdatetime.minute)
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
    #x_data, y_data, title, start_day, end_day = create_data()
    x_data_1, y_data_1, title_1, start_day_1, end_day_1 = create_data(csv_file_name_1)
    x_data_2, y_data_2, title_2, start_day_2, end_day_2 = create_data(csv_file_name_2) # 単純に繰り返してるが他方法試す

    fig = plt.figure(dpi=170)
    for j in range(graph_num):
        num = j + 1
        #ax = fig.add_subplot(graph_num, 1, num)
        ax = fig.add_subplot(1, 1, 1)

        # ax.set_major_locator(ticker.FixedLocator(x_data))
        # ax.set_major_formatter(DateFormatter('%H:%M'))
        #ax.tick_params(axis='x', rotation=270)

        graph_data1 = np.asfarray(y_data_1[num+1], dtype=float) #気温:2, 湿度:3, 絶対湿度:4
        graph_data2 = np.asfarray(y_data_2[num+1], dtype=float) #気温:2, 湿度:3, 絶対湿度:4
        #plt.xlabel(title[1])
        plt.xlabel('hour:minute')
        plt.xticks(rotation=270, fontsize=7)
        plt.ylabel(title_1[num+1])
        plt.plot(x_data_1, graph_data1, label='new_geek', linestyle='solid', marker='o')
        plt.plot(graph_data2, label='old_geek', linestyle='solid', marker='o')

        plt.ylim([min(plt.ylim())-0.5, max(plt.ylim())+0.5])
        plt.title(f'{start_day_1}~{end_day_1} {title_1[num+1]}')
        plt.legend(loc='upper right')
        plt.minorticks_on()

        plt.tight_layout()
        plt.savefig(os.path.join(image_file_path, image_file_name[j]))
        plt.close('all')

if __name__ == '__main__':
    create_graph()
