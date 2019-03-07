import numpy as np
import matplotlib.pyplot as plt
import square

R = 5
L = 5
V_p = 5
len = 1000
duty = 0.5
timeP = 1

t=np.linspace(0,10,len)
V=V_p*square.square(t, duty, timeP, len)
output_i=np.zeros(len)
#plt.plot(t,V)
for i in range(1000):
    #V[0]=5
    if t[i]%timeP<=duty*timeP:
        V[i]=(V[i])*(1-np.exp(-R*t[i]/L))
        output_i[i]=V[i]/R
    else:
        V[i]=V[i-1]*(np.exp(-R*t[i]/L))
        output_i[i]=V[i]/R
plt.plot(t, output_i)
#plt.ylim(0,1)
#plt.xlim(1.4,1.6)
