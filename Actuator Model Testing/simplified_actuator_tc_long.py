import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import tc_step_sampling as tc
import time as timer

start = timer.time()


def w_dot_BI(current, b):   # defining the dynamics for the system
    v_mu = No_Turns*np.multiply(v_A_Torquer, current)   # mu = I*A*n
    v_w_dot = np.cross(v_mu, b)     # torque = mu x B
    return v_w_dot      # w_dot = torque


def getMag_b(time):     # defining the magnetic field in the body frame(constant in the body frame so that we can integrate analytically)
    v_mag_b = np.array([1, 2, 3])*1e-3      # B =(1e-3, 2e-3, 3e-3)
    return v_mag_b


I0 = np.zeros(3)    # initial current is 0
time_period = 1/PWM_FREQUENCY
num_steps = 2
w_initial = np.zeros((1, 4))    # w_initial = 0
num_cycles_per_step = int(CONTROL_STEP/time_period)

for i in range(0, num_steps):
    w_array = w_initial     # initialising angular velocity for the control step
    time = np.array([i*2])      # initialising the time array for the control step
    duty = np.array([i+1, (-1**i)*(i+2), i+3])*1e-3     # initialising the duty cycle

    timeArr = tc.getTimeArr(duty)   # getting the time array for one PWM cycle
    num_instants_per_cycle = len(timeArr)
    for j in range(0, num_cycles_per_step):
        time = np.concatenate((time, timeArr+j*time_period))    # setting the time array for the whole step

    edgeCurrentArray = aac.getEdgeCurrent(duty, I0)     # getting the current at the edges

    for j in range(0, num_cycles_per_step):
        print("step ", i+1, " cycle ", j)
        for k in range(j*num_instants_per_cycle, (j+1)*num_instants_per_cycle):
            intTimeArr1 = np.linspace(time[k]%2, time[k+1]%2, 3, endpoint=True)      # setting the time array for the integration step
            intTimeArr = np.linspace(time[k], time[k+1], 3, endpoint=True)      
            currentArray = aac.getCurrentList(duty, intTimeArr1, 3, edgeCurrentArray)    # getting the current for the integration cycles
            h = time[k + 1] - time[k]
            k1 = w_dot_BI(currentArray[0], getMag_b(intTimeArr[0])) * h
            k2 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k3 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k4 = w_dot_BI(currentArray[2], getMag_b(intTimeArr[2])) * h
            angular_velocity_new = np.hstack((time[k+1] + i*CONTROL_STEP, w_array[k, 1:4]+(k1+2*k2+2*k3+k4)/6))
            w_array = np.vstack((w_array, angular_velocity_new))
    I0 = edgeCurrentArray[len(edgeCurrentArray) - 1]
    w_initial = np.array([w_array[len(w_array)-1]])
    np.savetxt("simplified_actuator_tc_long_data_cycle_%d.csv"%i, w_array[:, :], delimiter=",")
end = timer.time()
print(end-start)
