# -*- coding: utf-8 -*-
import Adafruit_DHT
import csv

PIN = 23

count = 0

dht_sensor = Adafruit_DHT.DHT11

while True:
    try:
        #for i in range(5): #代わりにRaspberry Piを再起動させて、その時に実行
        while True:

            humi, temp = Adafruit_DHT.read_retry(dht_sensor, PIN)

            #print("+", date, time)
            print("| 温度=",temp,"度")
            print("| 湿度=",humi, "%")

        #20分ごとにデータを取得
        #sleep(1200)

    except Exception as e:
        if(count<4):
            error = str('Error: ')+str(e)
            #slack.notify(text=error)
            print(error)
            count=count+1
            continue
        break

    # finally:
    #     #GPIO.cleanup()

    break
