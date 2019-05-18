import numpy as np
#import dynamics_actuator
#import solver
#import class_sat
import analytical_act_current as aac
#import TorqueApplied
from constants_1U import CONTROL_STEP, PWM_FREQUENCY
#import time as timer

#start = timer.time()

#sat = class_sat.Satellite(np.array([0, 0, 0, 1, 0, 0, 0]), 0)

#sat.setRequiredTorque(0)
#Mag_i = np.array([1,1,1])*1e-4
#sat.setMag_i(Mag_i)
#sat.setPos(np.array([1,1,1]))
#sat.setVel(np.array([1,1,2]))
#voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
#duty_cycle = voltageRequired/3.3

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
for i in range(0, num_cycles):
    time = np.concatenate((time, timeArr + i / PWM_FREQUENCY))

current_applied = np.zeros((3, 3))
edgeCurrentList = aac.getEdgeCurrent(duty_cycle, np.zeros(3))
state_array = np.zeros((num_instants + 1, 7))
start_1 = timer.time()
for i in range(0, num_instants):
    current_applied = aac.getCurrentList(duty_cycle, np.linspace(time[i], time[i+1], 3, endpoint=True), 3, np.zeros(3))
    torque_applied = TorqueApplied.currentToTorque(current_applied, sat)
    solver.rk4Quaternion(sat, dynamics_actuator.x_dot_BO, time[i+1]-time[i], torque_applied)
    state_array[i, :] = sat.getState()
    if i % 300 == 0:
        print(i/300, "%")
        end_1 = timer.time()
        print(end_1 - start_1)
np.savetxt("aac_test_variable_step.csv", state_array[:, :], delimiter=",")
end = timer.time()
print(-start + end)