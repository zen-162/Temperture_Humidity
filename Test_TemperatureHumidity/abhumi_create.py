import pandas as pd
import numpy as np
import csv
from decimal import ROUND_HALF_UP, Decimal

input_file_name = '/home/zen/Documents/Geek/TemperatureHumidity/temp_humi.csv'
output_file_name = '/home/zen/Documents/Geek/TemperatureHumidity/test_temp_humi.csv'

absolute_humis = []


def str2float(data):
    try:
        return float(data)
    except:
        return 0

with open(input_file_name) as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

    with open(output_file_name, 'a') as output_f:
        writer = csv.writer(output_f, lineterminator='\n')

        rows = np.array(rows).T # 転置
        #print('rows: ', rows)

        for index, row in enumerate(rows):
            if index == 0:
                writer.writerow(row)
                continue
            elif row == []:
                writer.writerow('')
                continue

            #print('row[2]: ', row[2])
            temp = str2float(row[2])
            humi = str2float(row[3])

            absolute_humi = 217*(6.1078*10**(7.5*temp/(temp+237.3)))/(temp+273.15)*humi/100
            a_absolute_humi = Decimal(str(absolute_humi))
            str_absolute_humi = a_absolute_humi.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            absolute_humi = float(str_absolute_humi)

            data = np.append(row, absolute_humi)

            #print('row: ', row)
            #print('absolute_humis: ', data)

            #datas = np.append(row, absolute_humis)

            writer.writerow(data)



# absolute_humi = 217*(6.1078*10**(7.5*temp/(temp+237.3)))/(temp+273.15)*humi/100
# a_absolute_humi = Decimal(str(absolute_humi))
# str_absolute_humi = a_absolute_humi.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
# absolute_humi = float(str_absolute_humi)
