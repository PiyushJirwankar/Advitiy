import analytical_act_current as aac
from constants_1U import CONTROL_STEP, PWM_FREQUENCY, PWM_AMPLITUDE as V_max, v_A_Torquer, RESISTANCE as R, INDUCTANCE as L, No_Turns
import numpy as np


T_P = 1/PWM_FREQUENCY
v_w_BI_b = np.zeros((1, 3))
NUM_STEPS = 2
I0 = np.zeros(3)
NUM_CYCLES_PER_STEP = int(CONTROL_STEP/T_P)


def integral_current_step(v_duty_cycle, v_edgeCurrent):
    v_duty_cycle = np.absolute(v_duty_cycle)
    res = V_max*T_P*v_duty_cycle/R
    res = res - V_max*L/R/R*(np.exp(-R*T_P/L*(1-v_duty_cycle)) - np.exp(-R*T_P/L))
    res = res + v_edgeCurrent*L/R*(1-np.exp(-R*T_P/L))
    res = np.cross(res, np.array([1, 2, 3])*1e-3)
    return res


for i in range(0, NUM_STEPS):
    v_duty = np.array([i+1, (-1**i)*(i+2), i+3])*1e-3
    edgeCurrent = aac.getEdgeCurrent(v_duty, I0)
    for j in range(0, NUM_CYCLES_PER_STEP):
        angular_velocity = v_w_BI_b[i*NUM_CYCLES_PER_STEP+j] + v_A_Torquer[0]*No_Turns*integral_current_step(v_duty, edgeCurrent[2*j])
        v_w_BI_b = np.vstack((v_w_BI_b, angular_velocity))
    I0 = edgeCurrent[len(edgeCurrent) - 1]
v_w_BI_b = v_w_BI_b * v_A_Torquer[0]*No_Turns
np.savetxt("simplified_actuator_true_long_data_2.csv", v_w_BI_b[:, :], delimiter=",")