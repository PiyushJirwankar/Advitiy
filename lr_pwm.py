import numpy as np
import matplotlib.pyplot as plt
import square

R = 5
L = 500
V_p = 5
len = 1000
duty = 0.5
timeP = 1

t_start = 0
t_end = 10
t=np.linspace(t_start,t_end,len)
h=10/(len-1)

V=V_p*square.square(t, duty, timeP, len)
output_i=np.zeros(len)
#plt.plot(t,V)
i_out = np.zeros(len)

'PWM volatage starts with high'

for i in range(1,len):
    if t[i]%timeP<=duty*timeP:
        x=(len/(t_end - t_start))*timeP
        #n=i%x
        i_out[i]=V_p*(1-np.exp(-(t[i]-t_start)*R/L))/R + i_out[i-1]*(np.exp(-(t[i]-t_start)*R/L))
    else:
        V[i]=V[i-1]
        V[i]=V[i-1]*(np.exp(-R*t[i]/L))
        output_i[i]=V[i]/R
plt.plot(t, i_out)
