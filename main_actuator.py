import numpy as np
import dynamics_actuator
import RK4
import class_sat

sat = class_sat.Satellite

v_x_q_dot_BO_k = dynamics_actuator.x_dot_BO(sat)[0:4]          #derivative of state vector (quaternion) at k th time instnat
v_x_w_dot_BO_b_k = dynamics_actuator.x_dot_BO(sat)[4:7]        #derivative of state vector (w_BO_b) at k th time instant

v_x_q_BO_knext = RK4.RK4(v_x_q_dot_BO_k, )