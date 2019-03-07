import numpy as np
import matplotlib.pyplot as plt
import square

R = 5
L = 5000
V_p = 5
len = 1000
duty = 0.5
timeP = 10

t_start = 0
t_end = 10

t=np.linspace(t_start,t_end,len)
h=int((t_end-t_start)/(len))

V=V_p*square.square(t, duty, timeP, len)

i_out = np.zeros(len)

for i in range(1,len):
    #V[0]=5
    if t[i]%timeP<=duty*timeP:                            #'PWM volatage starts with high'
        i_out[i] = (V_p - (V_p-i_out[i-1]*R)*(np.exp(-(t[i]-t_start)*R/L)))/R
    #    i_out[i]=V_p*(1-np.exp(-t[i]*R/L))/R + i_out[i-1]*(np.exp(-t[i]*R/L))
    #else:
    #    V[i]=V[i-1]
    #    V[i]=V[i-1]*(np.exp(-R*t[i]/L))
    #    output_i[i]=V[i]/R
plt.plot(t, i_out)
#plt.ylim(0,0.05)
#plt.xlim(0,0.5)
