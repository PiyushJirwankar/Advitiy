import numpy as np
import dynamics_actuator
import solver
import class_sat
import analytical_act_current as aac
import TorqueApplied
from constants_1U import CONTROL_STEP, PWM_FREQUENCY
import time as timer

start = timer.time()

sat = class_sat.Satellite(np.array([0, 0, 0, 1, 0, 0, 0]), 0)

sat.setRequiredTorque(0)
Mag_i = np.array([1,1,1])*1e-4
sat.setMag_i(Mag_i)
sat.setPos(np.array([1,1,1]))
sat.setVel(np.array([1,1,2]))
voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
duty_cycle = voltageRequired/3.3

n = 15
min_duty = np.abs(np.amin(duty_cycle))
max_duty = np.abs(np.amax(duty_cycle))
mid_duty = duty_cycle[0] + duty_cycle[1] + duty_cycle[3] - min_duty - max_duty
denom_t = 1.0/min_duty + 1.0/max_duty + 1.0/mid_duty + 10
time_arr_a = np.linspace(min_duty/PWM_FREQUENCY)
current_applied = np.zeros((3, 3))
edgeCurrentList = aac.getEdgeCurrent(duty_cycle, np.zeros(3))
state_array = np.zeros((100001, 7))
start_1 = timer.time()
for i in range(0, CONTROL_STEP*PWM_FREQUENCY*15):
    current_applied = aac.getCurrentList(duty_cycle, np.linspace(time[i], time[i+1], 3, endpoint=True), 3, np.zeros(3))
    torque_applied = TorqueApplied.currentToTorque(current_applied, sat)
    solver.rk4Quaternion(sat, dynamics_actuator.x_dot_BO, time[i+1]-time[i], torque_applied)
    state_array[i, :] = sat.getState()
    if(i%100==0):
        print(i/100, "%")        
        end_1 = timer.time()
        print(end_1 - start_1)
np.savetxt("aac_test.csv", state_array[:, :], delimiter=",")
end = timer.time()
print(start - end)