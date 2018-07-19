import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
tau_not=0.034  # sec
df=pd.read_csv('10min_gyro_data')
time=df['time'] 
with open('data.txt') as inputfile:
    columns = [line.split() for line in inputfile]  #rows=[line.split.....]

#columns = zip(*rows)
 
N=9
n=4
#A=np.zeros(q, dtype=float)
final=np.zeros(n , dtype=float)

mylist0=range(n+1)
mylist0.remove(0)

def theta(x,y):
    sum=0
    for i in range(x):
        sum = sum + float(columns[i][0])*tau_not         #columns[y][i]
    return sum

for i in mylist0:
    sum = 0
    mylist1=range(N-2*i+1)
    mylist1.remove(0)
    for k in mylist1:
        sum=sum+((theta(k+2*i,0)-2*theta(k+i,10)+theta(k,0))**(2))/(2*(i**(2))*((tau_not)**(2)*(N-2*i)))
    final[i-1]=np.log10(np.sqrt(sum))
print(np.sqrt(sum))

#x=np.linspace(np.log10(tau_not), np.log10(n*tau_not), n)
#plt.plot(x,final)
#plt.show()
