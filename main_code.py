# we start code by importing modules needed in the code

import appr_actuator as act
from constants_1U import *
#import controller as con
import default_blocks as defblock
import disturbance_1U as dist
from dynamics import x_dot_BO
from J2_propagator import propagate
import frames as fs
import math
import numpy as np
import os
import qnv
import satellite
import sensor
import solver as sol
import matplotlib.pyplot as plt
from test_cases import * 

#Read position, velocity, sun-vector, light-boolean, magnetic field (in nanoTeslas) in ECIF from data file

if (orbitbool==0):
	#get data for PO orbit
	m_sgp_output_temp_i = np.genfromtxt('sgp_output_PO.csv', delimiter=",")
	m_si_output_temp_b = np.genfromtxt('si_output_PO.csv',delimiter=",")
	m_light_output_temp = np.genfromtxt('light_output_PO.csv',delimiter=",")
	m_magnetic_field_temp_i = np.genfromtxt('mag_output_i_PO.csv',delimiter=",") 

if (orbitbool==1):
	#get data for SSO orbit
	m_sgp_output_temp_i = np.genfromtxt('sgp_output_SSO.csv', delimiter=",")
	m_si_output_temp_b = np.genfromtxt('si_output_SSO.csv',delimiter=",")
	m_light_output_temp = np.genfromtxt('light_output_SSO.csv',delimiter=",")
	m_magnetic_field_temp_i = np.genfromtxt('mag_output_i_SSO.csv',delimiter=",") 

count = 0 # to count no. of transitions from light to eclipses
init,end = 1, 0
'''
for k in range(0,len(m_light_output_temp)-2): #we go to k=length-2 only because maximum index for an array is length-1 and l2 = aaray[k+1]
	#obtain index corresponding to the start of eclipse
	l1 = m_light_output_temp[k,1]
	l2 = m_light_output_temp[k+1,1]
	if l1 ==1 and l2 == 0.5 and count == 0:	#start of first eclipse
		init = k
		count = 1
		
	elif l1==1 and l2==0.5 and count == 1:	#start of second eclipse
		end = k 
		break
'''
end = init +60000
#define simulation parameters
#print (init)
#print (end)


t0 = m_sgp_output_temp_i[init,0]
tf = m_sgp_output_temp_i[end,0]	   #tf-t0 represents simulation time in seconds
h = 0.1		                       #step size of integration in seconds  

if(int((tf-t0)/MODEL_STEP)*MODEL_STEP == (tf-t0)):
    Nmodel = int((tf-t0)/MODEL_STEP)
else :
    Nmodel = int((tf-t0)/MODEL_STEP)+1 #no. of time environment-cycle will run
print("tf=", tf, "t0=", t0, "Nmodel = ", Nmodel, "MODEL_STEP =", MODEL_STEP)
if(int((tf-t0)/CONTROL_STEP)*CONTROL_STEP == (tf-t0)):
    Ncontrol = int((tf-t0)/CONTROL_STEP)
else :
    Ncontrol = int((tf-t0)/CONTROL_STEP)+1 #no. of time control-cycle will run
print("Ncontrol = ", Ncontrol, "CONTROL_STEP", CONTROL_STEP)

#extract init to end data from temp file
m_sgp_output_i = m_sgp_output_temp_i[init:(init+Nmodel),:].copy()
m_si_output_b = m_si_output_temp_b[init:(init+Nmodel),:].copy()
m_light_output = m_light_output_temp[init:(init+Nmodel),:].copy()
m_magnetic_field_i = m_magnetic_field_temp_i[(init-1):(init+Nmodel)+30,:].copy() #changed : added +1 (30)
print (Nmodel ,'Simulation for ' ,MODEL_STEP*(Nmodel-1),'seconds')

#initialize empty matrices which will be needed in this simulation
m_state = np.zeros((Nmodel+1,7))
m_euler = np.zeros((Nmodel+1,3))
m_w_BI_b = np.zeros((Nmodel,3))
torque_dist_total = np.zeros((Nmodel,3))
torque_dist_gg = np.zeros((Nmodel,3))
torque_dist_aero = np.zeros((Nmodel,3))
torque_dist_solar = np.zeros((Nmodel,3))
torque_control = np.zeros((Nmodel,3))

#defining initial conditions
#initial state based on initial qBO and wBOB
#perfectly aligned body frame and orbit frame (v_q0_BO is initial value defined in constants)
#Body frame is not rotating wrt orbit frame (v_w0_BOB is initial value defined in constants)
m_state[0,:] = np.hstack((v_q0_BO,v_w0_BOB))                         
m_euler[0,:] = qnv.quat2euler(v_q0_BO)    #finding initial euler angles

#Make satellite object
Advitiy = satellite.Satellite(m_state[0,:],t0)   #t0 from line 42 of main_code
Advitiy.setPos(m_sgp_output_i[0,1:4])
Advitiy.setVel(m_sgp_output_i[0,4:7])
Advitiy.setLight(m_light_output[0,1])
Advitiy.setTime(t0) #time at a cycle 
Advitiy.setSun_i(m_si_output_b[0,1:4])
Advitiy.setMag_i(m_magnetic_field_i[0,1:4])
Advitiy.setMag_b_m_c(defblock.magnetometer(Advitiy))

time_gps = 10 #min   This time must be an interal multiple of CONTROL_STEP
time_J2 = 10 #min    This time must be an interal multiple of CONTROL_STEP

i_time_gps = 10*60/CONTROL_STEP
i_time_J2 = 10*60/CONTROL_STEP

#-------------Main for loop---------------------
for  i in range(0,Ncontrol):  #loop for control-cycle
	
	if math.fmod(i,int(Ncontrol/100)) == 0: #we are printing percentage of cycle completed to keep track of simulation
		print (int(100*i/Ncontrol)) 

	if (i%(i_time_gps+i_time_J2) <= i_time_gps):
		propbool = 0
	else:
		propbool = 1     
    
	#sensor reading
	if (sensbool == 0):
		#getting default sensor reading (zero noise in our case)
		Advitiy.setSun_b_m(defblock.sunsensor(Advitiy))
		Advitiy.setMag_b_m_p(Advitiy.getMag_b_m_c())
		Advitiy.setMag_b_m_c(defblock.magnetometer(Advitiy))
		Advitiy.setgpsData(defblock.gps(Advitiy))
		Advitiy.setOmega_m(defblock.gyroscope(Advitiy))
#		Advitiy.setJ2Data(defblock.J2_propagator(Advitiy))

	if (sensbool == 1):
		#getting sensor reading from models
		Advitiy.setSun_b_m(sensor.sunsensor(Advitiy))
		Advitiy.setMag_b_m_p(Advitiy.getMag_b_m_c())
		Advitiy.setMag_b_m_c(sensor.magnetometer(Advitiy))
		Advitiy.setOmega_m(sensor.gyroscope(Advitiy))
        if (propbool == 0):
        #Using sgp to propagate
            Advitiy.setgpsData(sensor.GPS(Advitiy))    
            
        if (propbool == 1):
        #Use J2 to propagate
            pos = Advitiy.getPos_J2()
            vel = Advitiy.getVel_J2()
            Advitiy.setPos_J2(propagate(pos, vel, time_J2, 0.5, drag=False)[0])
            Advitiy.setVel_J2(propagate(pos, vel, time_J2, 0.5, drag=False)[1])
        
#		Advitiy.setJ2Data(sensor.J2_propagator(Advitiy))

	#Estimated quaternion
	if (estbool == 0): #qBO is same as obtained by integrator
		Advitiy.setQUEST(defblock.estimator(Advitiy))

	#if (estbool == 1): #qBO is obtained using Quest/MEKF

	#control torque
	
	if (contcons == 0):
		#getting default control torque (zero in our case)
		Advitiy.setControl_b(defblock.controller(Advitiy))
	
	if (contcons == 1):
		#getting control torque by omega controller 
         # k = 0.001
		torque_control[i*int(Nmodel/Ncontrol):(i+1)*(int(Nmodel/Ncontrol)),:] = -0.001*Advitiy.getW_BI_b()
		#print(Advitiy.getW_BI_b())
		Advitiy.setControl_b(torque_control[i*int(Nmodel/Ncontrol),:])

	#torque applied
	
	if (actbool == 0):
		#applied torque is equal to required torque
		Advitiy.setAppTorque_b(Advitiy.getControl_b())
        
	#if (actcons == 1):
		#getting applied torque by actuator modelling (magnetic torque limitation is being considered)

	for k in range (0,int(Nmodel/Ncontrol)):  #loop for environment-cycle
		#Set satellite parameters
		#state is set inside solver
		Advitiy.setPos(m_sgp_output_i[i*int(Nmodel/Ncontrol)+k,1:4])
		Advitiy.setVel(m_sgp_output_i[i*int(Nmodel/Ncontrol)+k,4:7])
		Advitiy.setLight(m_light_output[i*int(Nmodel/Ncontrol)+k,1])
		Advitiy.setTime(t0 + i*int(Nmodel/Ncontrol)+k) #time at a cycle 
		Advitiy.setSun_i(m_si_output_b[i*int(Nmodel/Ncontrol)+k,1:4])
		Advitiy.setMag_i(m_magnetic_field_i[(i+1)*int(Nmodel/Ncontrol)+k,1:4])
		

		# disturbance torque
		if (distbool == 0):
			#getting default disturbance torque (zero in our case)
			Advitiy.setDisturbance_b(defblock.disturbance(Advitiy))

		if (distbool == 1):
			#getting disturbance torque by disturbance model
			dist.ggTorqueb(Advitiy)
			dist.aeroTorqueb(Advitiy)
			dist.solarTorqueb(Advitiy)
			
			torque_dist_gg[i*int(Nmodel/Ncontrol)+k,:] = Advitiy.getggDisturbance_b()
			torque_dist_aero[i*int(Nmodel/Ncontrol)+k,:] = Advitiy.getaeroDisturbance_b()
			torque_dist_solar[i*int(Nmodel/Ncontrol)+k,:] = Advitiy.getsolarDisturbance_b()
			torque_dist_total[i*int(Nmodel/Ncontrol)+k,:] = torque_dist_gg[i*int(Nmodel/Ncontrol)+k,:] + torque_dist_aero[i*int(Nmodel/Ncontrol)+k,:] + torque_dist_solar[i*int(Nmodel/Ncontrol)+k,:]
			Advitiy.setDisturbance_b(torque_dist_total[i*int(Nmodel/Ncontrol)+k,:].copy())
			
		#Use rk4 solver to calculate the state for next step
		sol.updateStateTimeRK4(Advitiy,x_dot_BO,h)
		
		#storing data in matrices
		m_state[i*int(Nmodel/Ncontrol)+k+1,:] = Advitiy.getState()
		m_euler[i*int(Nmodel/Ncontrol)+k+1,:] = qnv.quat2euler(Advitiy.getQ_BO())
		m_w_BI_b[i*int(Nmodel/Ncontrol)+k,:]= Advitiy.getW_BI_b()
        
#save the data files
os.chdir('Logs-Detumbling/')
os.mkdir('trial35')
os.chdir('trial35')
np.savetxt('position.csv',m_sgp_output_i[:,1:4], delimiter=",")
np.savetxt('velocity.csv',m_sgp_output_i[:,4:7], delimiter=",")
np.savetxt('time.csv',m_sgp_output_i[:,0] - t0, delimiter=",")
np.savetxt('state.csv',m_state, delimiter=",")
np.savetxt('w_BI_b.csv',m_w_BI_b, delimiter=",")
np.savetxt('euler.csv',m_euler, delimiter=",")
np.savetxt('disturbance-total.csv',torque_dist_total, delimiter=",")
np.savetxt('disturbance-gg.csv',torque_dist_gg, delimiter=",")
np.savetxt('disturbance-solar.csv',torque_dist_solar, delimiter=",")
np.savetxt('disturbance-aero.csv',torque_dist_aero, delimiter=",")
np.savetxt('control torque.csv',torque_control, delimiter=",")


time_state = m_sgp_output_temp_i[init:(init+Nmodel+1),0]
time = m_sgp_output_i[:,0] - t0
state = m_state
euler = m_euler
pos = m_sgp_output_i[:,1:4]
vel = m_sgp_output_i[:,4:7]
dist = torque_dist_total

plt.figure(1)
plt.plot(time,pos[ : ,0],label='pos_x')
plt.plot(time,pos[ : ,1],label='pos_y')
plt.plot(time,pos[ : ,2],label='pos_z')
plt.title('position in meters')
plt.legend()
plt.savefig('position in meters')

plt.figure(2)
plt.plot(time,vel[ : ,0],label='vel_x')
plt.plot(time,vel[ : ,1],label='vel_y')
plt.plot(time,vel[ : ,2],label='vel_z')
plt.title('velocity in meters per second')
plt.legend()
plt.savefig('velocity')

plt.figure(3)
plt.plot(time_state,state[ : ,0],label='q1')
plt.plot(time_state,state[ : ,1],label='q2')
plt.plot(time_state,state[ : ,2],label='q3')
plt.plot(time_state,state[ : ,3],label='q4')
plt.title('qBO')
plt.legend()
plt.savefig('qBO')

plt.figure(4)
plt.plot(time_state,state[ : ,4],label='wBOB_x')
plt.plot(time_state,state[ : ,5],label='wBOB_y')
plt.plot(time_state,state[ : ,6],label='wBOB_z')
plt.title('wBOB in degrees')
plt.legend()
plt.savefig('wBOB')

plt.figure(5)
plt.plot(time_state,euler[:,0],label='roll')
plt.plot(time_state,euler[:,1],label='pitch')
plt.plot(time_state,euler[:,2],label='yaw')
plt.title("euler_BO in degrees")
plt.legend()
plt.savefig('euler_BO')

plt.figure(6)
plt.plot(time,torque_dist_total[:,0],label="t_x")
plt.plot(time,torque_dist_total[:,1],label="t_y")
plt.plot(time,torque_dist_total[:,2],label="t_z")
plt.legend()
plt.title('disturbance torque')
plt.savefig('disturbance torque')


plt.figure(7)
plt.plot(time,torque_control[:,0],label="t_x")
plt.plot(time,torque_control[:,1],label="t_y")
plt.plot(time,torque_control[:,2],label="t_z")
plt.legend()
plt.title('control torque')
plt.savefig('control torque')

plt.figure(8)
plt.plot(time,m_w_BI_b[:,0],label="wBIB_x")
plt.plot(time,m_w_BI_b[:,1],label="wBIB_y")
plt.plot(time,m_w_BI_b[:,2],label="wBIB_z")
plt.legend()
plt.title('wBIB')
plt.savefig('wBIB')
