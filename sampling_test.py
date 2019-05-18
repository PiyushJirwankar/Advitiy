import numpy as np
import matplotlib.pyplot as plt
import analytical_act_current as aac
from constants_1U import PWM_FREQUENCY, CONTROL_STEP


duty_cycle = np.array([0.1, 0.01, 0.001])
I0 = np.array([0., 0., 0.])

edge_current = aac.getEdgeCurrent(duty_cycle, I0)
N = 100001
current_list_true = np.zeros((N,3))


time_true = np.linspace(0, 2, N, endpoint=True)
current_list_true = aac.getCurrentList(duty_cycle, time_true, N, I0)

n_1=5
time_1 = np.linspace(0, 2, (n_1*2000)+1, endpoint=True) #10 uniform steps in one PWM cycle
current_list_uniform_steps = aac.getCurrentList(duty_cycle, time_1, (n_1*2000)+1, I0)

m=10*2000
current_list_vaiable_spacing = np.zeros((m,3))


n = 15
min_duty = np.abs(np.amin(duty_cycle))
max_duty = np.abs(np.amax(duty_cycle))
mid_duty = np.abs(duty_cycle[0] + duty_cycle[1] + duty_cycle[2] - min_duty - max_duty)

time_a = min_duty / PWM_FREQUENCY
time_b = mid_duty / PWM_FREQUENCY - time_a
time_c = max_duty / PWM_FREQUENCY - time_a - time_b
time_d = (1 - max_duty) / PWM_FREQUENCY

denom_t = 1.0/min_duty + 1.0/max_duty + 1.0/mid_duty + 10
num_a = int((1 / min_duty) * n / denom_t)
num_b = int((1 / mid_duty) * n / denom_t)
num_c = int((1 / max_duty) * n / denom_t)
num_d = n - num_a - num_b - num_c

timeArr_a = np.linspace(time_a/num_a, time_a, num_a, endpoint=True)
timeArr_b = np.linspace(time_a + time_b/num_b, time_a + time_b, num_b, endpoint=True)
timeArr_c = np.linspace(time_a + time_b + time_c/num_c, time_a + time_b + time_c, num_c, endpoint=True)
timeArr_d = np.linspace(time_a + time_b + time_c + time_d/num_d, time_a + time_b + time_c + time_d, num_d, endpoint=True)

num_cycles = int(CONTROL_STEP * PWM_FREQUENCY)
num_instants = int(num_cycles * n)
timeArr = np.concatenate((timeArr_a, timeArr_b, timeArr_c, timeArr_d))
time = np.zeros(1)
#current_variable_step = np.zeros((30001, 3))
for i in range(0, num_cycles):
    time = np.concatenate((time, timeArr + i / PWM_FREQUENCY))

current_applied = np.zeros((30001, 3))
edgeCurrentList = aac.getEdgeCurrent(duty_cycle, np.zeros(3))
state_array = np.zeros((num_instants + 1, 7))
for i in range(0, num_instants):
    current_applied = aac.getCurrentList(duty_cycle, np.linspace(time[i], time[i+1], 30001, endpoint=True), 3, np.zeros(3))
print(current_applied)
'''
plt.plot(time_1, current_list_uniform_steps[:, 0], color='r')
plt.plot(time_1, current_list_uniform_steps[:, 1], color='r')
plt.plot(time_1, current_list_uniform_steps[:, 2], color='r')

plt.hold
plt.plot(time_true, current_list_true[:, 0], color='g')
plt.plot(time_true, current_list_true[:, 1], color='g')
plt.plot(time_true, current_list_true[:, 2], color='g')

plt.hold


plt.xlim(-0.005, 0.005)
'''