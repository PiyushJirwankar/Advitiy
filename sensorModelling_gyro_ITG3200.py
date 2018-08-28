#The following code will be used for sensor modelling of the gyroscope ITG3200
import numpy as np
import pandas as pd
import random
#import decimal

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
#scale_factor = 14.375       #Sensitivity scale factor  resolution= 1/14.375= 0.069 degrees/sec
#startup_time = 50           #miliseconds
#FFT = 0.03                  #degrees/sec/ sq.root(Hz)        This is the rate noise spectral density at 10Hz
#ARW = (1/3600) * (FFT)      #refer the pdf on angle random walk
std_dev = 0.38  #degrees/sec     
'This value if std_dev is taken from datasheet'
var=(std_dev)**2
random_error_x = random.gauss(ZRO_x , var)  #Here we are assuming the std dev of the errors to be same for all three directions
random_error_y = random.gauss(ZRO_y , var)
random_error_z = random.gauss(ZRO_z , var)
#cross_axis_sensitivity = 0.02  #This can be included but its contribution is very less so not included to reduce the complexity of the code
# link to the above mentioned pdf for ARW
'https://drive.google.com/file/d/1Ek1Fu3psTNbRRQOpWl1nVOvNdKziTJw5/view?usp=sharing'
#cross_axis_sensitivity = 2% max

'output = actual_value + bias + bias_change_rate(ARW) + random_errors'
'ZRO can vary between -40 to 40 deg/sec but I am assuming it to be 0 here'

output_x=np.zeros(length)    #represents the actual rotational velocity about x direction
output_y=np.zeros(length)    #represents the actual rotational velocity about y direction
output_z=np.zeros(length)    #represents the actual rotational velocity about z direction

for i in range(length):
    output_x[i] = (actual_x[i] + random_error_x + ZRO_x)            #bias
    output_y[i] = (actual_y[i] + random_error_y + ZRO_y)            #bias
    output_z[i] = (actual_z[i] + random_error_z + ZRO_z)            #bias

'Above, bias is the rate random walk(the time varying bias of the gyro)' 

print(output_x)
#print(output_y)
#print(output_z)

'''
there is a possibility that the bias may change over time- which is known as bias instability.
This has not been accounted for here.
As of now, it is not clear if bias instability will substantially affect our modelling or not
'''