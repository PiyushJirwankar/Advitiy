import numpy as np
from qnv import quatDerBO, quat2rotm 
import frames
from constants_1U import m_INERTIA, v_w_IO_o, m_INERTIA_inv

def x_dot_BO(sat):    #need m_INERTIA (abot center of mass)
    '''
        This function calculates the derivative of quaternion (q_BO)
        and angular velocity w_BOB
        Input: satellite, time
        Output: Differential state vector
    '''
    #get torques acting about COM    #Disturbance torque
    v_disturbance_torque = 0
    v_control_torque = sat.getControl_b()
    v_torque_b = v_control_torque + v_disturbance_torque
    
    #get current state
    v_q_BO = sat.getQ_BO()  #unit quaternion rotating from orbit to body 
    v_w_BO_b = sat.getW_BO_b()  #angular velocity of body frame wrt orbit frame in body frame
    R = quat2rotm(v_q_BO)
    #Kinematic equation

    v_q_BO_dot = quatDerBO(v_q_BO,v_w_BO_b)   
    v_w_BI_b = frames.wBOb2wBIb(v_w_BO_b,v_q_BO,v_w_IO_o)
    v_w_OI_o = -v_w_IO_o.copy()

    #Dynamic equation - Euler equation of motion
    v_w_BO_b_dot = np.dot(m_INERTIA_inv, v_torque_b - np.cross(v_w_BI_b,np.dot(m_INERTIA,v_w_BI_b))) - (np.cross(np.dot(R, v_w_OI_o), v_w_BO_b))
    v_x_dot = np.hstack((v_q_BO_dot, v_w_BO_b_dot))

    return v_x_dot