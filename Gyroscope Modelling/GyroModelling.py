#The following code will be used for sensor modelling of the gyroscope ITG3200
import numpy as np
import pandas as pd
import random

'The data has been logged from ITG3200 for 10 minutes. The mean in x, y, z direction (ZRO) is taken to be the average of the corresponding data values'

df=pd.read_csv('10min_gyro_data.csv')
actual_x = df['output_x']
actual_y = df['output_y']
actual_z = df['output_z']
time     = df['time']
length   = len(df['time'])
# All the valuse that are being initialized are according to the datasheet of ITG3200
ZRO_x = -2.5899514          #(degrees/sec) zero rate output in x-direction
ZRO_y = -1.0843420          #(degrees/sec) zero rate output in y-direction
ZRO_z = 0.32033737          #(degrees/sec) zero rate output in z-direction
std_dev = 0.38  #degrees/sec     
'This value if std_dev is taken from datasheet'
var=(std_dev)**2
random_error_x = random.gauss(ZRO_x , var)  #Here we are assuming the std dev of the errors to be same for all three directions
random_error_y = random.gauss(ZRO_y , var)
random_error_z = random.gauss(ZRO_z , var)

'output = actual_value + bias + bias_change_rate(ARW) + random_errors'

def gyroOoutput(actual_x, actual_y, actual_z):
    length = len(actual_x)
    output = np.zeros((length,3))
    for i in range(length):
        output[i,0] = 0    #represents the actual rotational velocity about x direction
        output[i,1] = 0    #represents the actual rotational velocity about y direction
        output[i,2] = 0    #represents the actual rotational velocity about z direction
    for i in range(length):
        output[i,0] = (actual_x[i] + random_error_x)            #bias
        output[i,1] = (actual_y[i] + random_error_y)            #bias
        output[i,2] = (actual_z[i] + random_error_z)            #bias
    return output

'Above, bias is the rate random walk(the time varying bias of the gyro)' 
