import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('10min_gyro_data.csv')
output_x=df['output_x']
output_y=df['output_y']
output_z=df['output_z']
time=df['time']
tau_not = 0.034  #sec
#N=len(time)     # N=21430
N = 101  
n = int(N/2)

def theta(x,y):           #x is till what number we want the sum
    sum=0   
    mylist2 = range(x+1)
    mylist2.remove(0)              #y is for which column we want (ie output_x or output_y or output_z)
    if y==0:
        for i in mylist2:
            sum = sum + output_x[i]*(time[i+1] - time[i])
    if y==1:
        for i in mylist2:
            sum = sum + output_y[i]*(time[i+1] - time[i])
    if y==2:
        for i in mylist2:
            sum = sum + output_z[i]*(time[i+1] - time[i])
    return sum

allan_dev_x = np.empty([n,1])
allan_dev_y = np.empty([n,1])
allan_dev_z = np.empty([n,1])
tau_values = np.linspace(tau_not, n*tau_not, n)

mylist0 = range(n+1)
mylist0.remove(0)

for i in mylist0:
    sum = 0
    mylist1 = range(N-2*i+1)
    mylist1.remove(0)
    for k in mylist1:
        sum = sum + ((theta(k+2*i, 0) - 2*theta(k+i,0) + theta(k,0))**(2))/(2*((i*tau_not)**(2))*(N-2*i))
    adev_x = np.sqrt(sum)
    allan_dev_x[i-1] = adev_x
    for k in mylist1:
        sum = sum + ((theta(k+2*i, 1) - 2*theta(k+i,1) + theta(k,1))**(2))/(2*((i*tau_not)**(2))*(N-2*i))
    adev_y = np.sqrt(sum)
    allan_dev_y[i-1] = adev_y
    for k in mylist1:
        sum = sum + ((theta(k+2*i, 2) - 2*theta(k+i,2) + theta(k,2))**(2))/(2*((i*tau_not)**(2))*(N-2*i))
    adev_z = np.sqrt(sum)
    allan_dev_z[i-1] = adev_z
 
plt.plot(np.log10(tau_values), np.log10(allan_dev_x) ,color='r', label='X-output')
plt.plot(np.log10(tau_values), np.log10(allan_dev_y) ,color='b', label='Y-output')
plt.plot(np.log10(tau_values), np.log10(allan_dev_z) ,color='g', label='Z-output')

plt.xlabel('Tau values')
plt.ylabel('Allan deviation')
plt.legend(['X-output', 'Y-output', 'Z-output'])