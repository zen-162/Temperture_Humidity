import pandas as pd
import numpy as np
import csv
from decimal import ROUND_HALF_UP, Decimal

input_file_name = '/home/zen/Documents/Geek/TemperatureHumidity/temp_humi.csv'
output_file_name = '/home/zen/Documents/Geek/TemperatureHumidity/test_temp_humi.csv'



with open(input_file_name) as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

    with open(output_file_name, 'a') as output_f:
        writer = csv.writer(output_f, lineterminator='\n')

        rows = np.array(rows).T # 転置

        for i in range(len(rows)):
            if i == 0:
                continue
            elif rows == []:
                writer.writerow('\n')
                continue

            print('rows[2]: ', rows[2])
            temp = float(rows[2])
            humi = float(rows[3])

            absolute_humi = 217*(6.1078*10**(7.5*temp/(temp+237.3)))/(temp+273.15)*humi/100
            a_absolute_humi = Decimal(str(absolute_humi))
            str_absolute_humi = a_absolute_humi.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            absolute_humi = float(str_absolute_humi)

            datas = np.append(rows, absolute_humi)

            writer.writerow(datas)



# absolute_humi = 217*(6.1078*10**(7.5*temp/(temp+237.3)))/(temp+273.15)*humi/100
# a_absolute_humi = Decimal(str(absolute_humi))
# str_absolute_humi = a_absolute_humi.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
# absolute_humi = float(str_absolute_humi)
