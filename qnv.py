import numpy as np

def quatInv(v_q1): #to get inverse of a quaternion
    new_q    =  v_q1[:]
    new_q[0] = -new_q[0]
    new_q[1] = -new_q[1]
    new_q[2] = -new_q[2]
    new_q[3] =  new_q[3]
    return new_q


def quat2rotm(v_q): #given a quaternion it returns a rotation matrix
    qx = v_q[0]
    qy = v_q[1]
    qz = v_q[2]
    q0 = v_q[3]

    m_M1 = 2* np.array([[qx**2,qx*qy,qx*qz],[qx*qy,qy**2,qy*qz],[qx*qz,qy*qz,qz**2]])
    m_M2 = -2*q0*np.array([[0,-qz,qy],[qz,0,-qx],[-qy,qx,0]])
    m_M3 = (2*((q0)**2)-1)*np.identity(3)
    return m_M1 + m_M2 + m_M3 
