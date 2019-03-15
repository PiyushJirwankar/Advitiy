import numpy as np
import matplotlib.pyplot as plt
import actuator_variablePWM as act_variable
import actuator as act
import constants_1U
from constants_1U import RESISTANCE, INDUCTANCE, PWM_AMPLITUDE, PWM_FREQUENCY, CONTROL_STEP
import constants_1U_variablePWM
from constants_1U_variablePWM import n
import math

v_duty = np.array([0.5,0.7,0.2])
h=0.002
i_list = act.getCurrentList(h,v_duty)
N=int(CONTROL_STEP/h)
t=np.zeros(N)
i3=np.zeros(N)
i2=np.zeros(N)
i1=np.zeros(N)
t=i_list[:,0]
i1=i_list[:,1]
i2=i_list[:,2]
i3=i_list[:,3]

plt.plot(t,i1,'r')
#plt.xlim(1,1.1)
plt.plot(t,i2,'b')
plt.plot(t,i3,'g')
#plt.xlim(0,0.25)