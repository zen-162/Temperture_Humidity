# -*- coding: utf-8 -*-
from time import sleep
import datetime
import Adafruit_DHT
import slackweb

from decimal import ROUND_HALF_UP, Decimal

import test_create_csv as create_csv

PIN = 23

#slack proj-temperature_humidity
slack = slackweb.Slack(url='https://hooks.slack.com/services/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')

count=0
#dht_device = adafruit_dht.DHT11(PIN)
dht_sensor = Adafruit_DHT.DHT22
#humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, PIN)

while True:
    try:
        #for i in range(5): #代わりにRaspberry Piを再起動させて、その時に実行
        while True:
            #temp = dht_device.temperature
            #temp = temperature
            #humi = dht_device.humidity
            #humi = humidity
            #result = instance.read()
            #temp = result.temperature
            #humi = result.humidity
            humi, temp = Adafruit_DHT.read_retry(dht_sensor, PIN)
            a_temp = Decimal(str(temp))
            a_humi = Decimal(str(humi))

            str_temp = a_temp.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            str_humi = a_humi.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

            temp = float(str_temp)
            humi = float(str_humi)
            #異常な値なら再取得
            if ((humi > 90) or (temp > 50)):
                print('- error:', temp, humi)
                sleep(0.1)
                continue
            break

        date = datetime.datetime.now().strftime('%Y/%m/%d')
        time = datetime.datetime.now().strftime('%H:%M:%S')

        print("+", date, time)
        print("| 温度=",temp,"度")
        print("| 湿度=",humi, "%")

        #絶対温度
        absolute_humi = 217*(6.1078*10**(7.5*temp/(temp+237.3)))/(temp+273.15)*humi/100
        a_absolute_humi = Decimal(str(absolute_humi))
        str_absolute_humi = a_absolute_humi.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        absolute_humi = float(str_absolute_humi)

        #CSV Fileに書き込み
        ldate = [date, time]
        ldata = [temp, humi, absolute_humi]
        #datas = [date, time, temp, humi]
        # with open(csv_file_name, 'a') as exf:
        #     writer = csv.writer(exf, lineterminator='\n')
        #     writer.writerow(ldate+ldata)
        datas = ldate + ldata
        create_csv.create_csv(datas)

        #Slackに通知
        data = date+' '+time+'\r\n 気温：' + str(temp) + '℃　湿度：' +str(humi) + '％ 絶対湿度: ' + str(absolute_humi) +'\r\n'
        temp_data = data
        #slack.notify(text=temp_data)

        #20分ごとにデータを取得
        #sleep(1200)

    except Exception as e:
        if(count<4):
            error = str('Error: ')+str(e)
            #slack.notify(text=error)
            print(error)
            #print(traceback.format_exc())
            count=count+1
            continue
        break

    # finally:
    #     #GPIO.cleanup()

    break
