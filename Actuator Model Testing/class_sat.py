from constants_1U import *

import numpy as np
import frames as fs

class Satellite:

    # units followed
    # magnetic field is in nanoTesla
    # position and velocity of satellite in SI units
    def __init__(self,v_state0,time0):

        self.setTime(time0)
        self.setState(v_state0)

    def setState(self,v_state1):	#set state

        self.v_state = v_state1.copy()

    def getState(self):	#returns the state

        return self.v_state

    def setPos(self,v_pos):	#set position in eci (earth centered inertial frame)
        self.v_pos_i = v_pos.copy()

    def getPos(self):	#return position in eci
        return self.v_pos_i

    def setVel(self,v_vel):	#set velocity in eci
        self.v_vel_i = v_vel.copy()

    def getVel(self):	#get velocity in eci
        return self.v_vel_i

    def setQ_BO(self,v_q):	#set error quaternion from orbit frame to body frame
        self.v_state[0:4]=v_q.copy()

    def getQ_BO(self):	#get error quaternion from orbit frame to body frame
        return self.v_state[0:4]

    def getQ_BI(self):	#get exact quaternion from inertial frame to body frame
        v_q_BI = fs.qBO2qBI(self.v_state[0:4],self.v_pos_i,self.v_vel_i)
        return v_q_BI

    def setW_BO_b(self,v_w):	#set exact angular velocity of body with respect to orbit expressed in body frame
        self.v_state[4:7]=v_w.copy()

    def getW_BO_b(self):	#get exact angular velocity of body with respect to orbit expressed in body frame
        return self.v_state[4:7]

    def getW_BI_b(self): #get exact angular velocity of body frame with respect to inertial frame expressed in body frame
        v_w_BO_b = self.v_state[4:7]
        v_q_BO = self.v_state[0:4]
        v_w_BI_b = fs.wBOb2wBIb(v_w_BO_b,v_q_BO,v_w_IO_o) #calculation of wBIb from wBOb stored in frames using wBOb2wBIb (function of frames) (v_w_IO_o from constants_1U)
        return v_w_BI_b

    def setTime(self,y):	#set time
        self.time = y

    def getTime(self):	#return time
        return self.time

    def setDisturbance_b(self,v_torque_dist_b):	#set disturbance in body (about center of mass)
        self.v_dist_b = v_torque_dist_b.copy()
        
    def getDisturbance_b(self):	#return disturbance in body
        return self.v_dist_b

    def setRequiredTorque(self, t):
        self.requiredTorque = np.array([1, 1, 1])*1e-8

    def getRequiredTorque(self):
        return self.requiredTorque

    def setControl_b(self,v_control):	#set control torque in body
        self.v_control_b = v_control.copy()

    def getControl_b(self): #return control torque in body
        return self.v_control_b

    def setMag_i(self,v_mag_i):	#set mag in eci
        self.v_mag_i = v_mag_i.copy()

    def getMag_i(self):	#return mag in eci
        return self.v_mag_i

    def getMag_o(self):	#return mag in orbit
        v_mag_o = fs.ecif2orbit(self.v_pos_i,self.v_vel_i,self.v_mag_i)
        return	v_mag_o

    def setMagmomentRequired_b(self,v_req_Magmoment_b): #set magnetic moment required by controller in body frame
        self.v_req_Magmoment_b=v_req_Magmoment_b

    def getMagmomentRequired_b(self):                #get magnetic moment required by controller in body frame
        return self.v_req_Magmoment_b

    def setAppTorque_b(self,v_app_torque_b): #set applied torque
        self.v_app_torque_b=v_app_torque_b

    def getAppTorque_b(self):                #get applied torque
        return self.v_app_torque_b