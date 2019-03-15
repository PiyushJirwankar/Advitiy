#Constants used in the code for simulation of 1U satellite

import numpy as np
import datetime as dt
from math import sqrt, sin, radians

AU = 149597870700.0 #Distance between sun and earth in meters
R_SUN = 6957e5 #Radius of the Sun in meters
#--------Earth and environment
W_EARTH = 7.2921150e-5; # rotation velocity of the earth (rad per second)
G = 6.67408e-11; #universal gravitational constant, SI
M_EARTH = 5.972e24; #mass of earth, kg
R_EARTH = 6371.0e3; #radius of earth, m
ALTITUDE = 700e3 # (in m) assunming height of satellite 700 km
V_R_B_COE = R_EARTH + ALTITUDE #Distance of satellite from center of earth m
v_w_IO_o = np.array([0., np.sqrt(G*M_EARTH/(V_R_B_COE)**3), 0.]) #angular velocity of orbit frame wrt inertial frame in orbit frame
AU = 149597870700.0 #Distance between sun and earth in meters
R_SUN = 6957e5 #Radius of the Sun in meters

#------------date format yyyy,mm,dd (TLE taken from n2yo.com on 3rd April)
LINE1 = ('1 41783U 16059A   18093.17383152  .00000069  00000-0  22905-4 0  9992') #Insert TLE Here
LINE2 = ('2 41783  98.1258 155.9141 0032873 333.2318  26.7186 14.62910114 80995') 
'''
#For Polar orbit
Eccen = 0
Incl_deg =90
'''
### add TT and dT in constants
TT = 200.0 # total time in minutes   ##add in constant
dT = np.linspace(0.0,TT*60.0,(TT*60*10 + 1)) #np.linspace(0.0,TT*60.0,(100*60*10 + 1)) ## dT is in seconds. total 100 minutes here. 10 is for 1/timestep
####ADDED following block ......these data based on spacetrack report3 page 81
MeanMo = 14.62910114  #16.05824518
Eccen = 0.0032873     # 0.0086731
Incl_deg =98.1258
MeanAnamoly_deg = 26.7186  #110.5714
ArgP = 333.2318 #52.6988
RAAN_deg = 155.9141  # 115.9689
DMeanMotion =0.00000069
DDMeanMotion =0
BStar = 0.22905e-4 #7e-07

TPer = LINE2[52:63]
TiPer = float("".join(map(str, TPer)))
TimePeriod = 86400/TiPer

EPOCH = dt.datetime(2018, 4, 3, 12, 50, 19)	#date of launch t=0
EQUINOX = dt.datetime(2018, 3, 20, 13, 5, 00)	#day of equinox
STEPRUT = 1.002738 #sidereal time = stperut * universal time

#-- --------Moment of inertia matrix in kgm^2 for 1U satellite (assumed to be uniform with small off-diagonal) (wrt center of mass)
MASS_SAT = 0.79211825320	#in kg
Lx = 0.1 #in meters
Ixx = 0.00152529
Iyy = 0.00145111
Izz = 0.001476
Ixy = 0.00000437
Iyz = - 0.00000408
Ixz = 0.00000118

#m_INERTIA = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]])	#actual inertia
m_INERTIA = np.array([[1.0,0.,0.],[0.,1.,0.],[0.,0.,1.]])	#identity inertia

m_INERTIA_inv = np.linalg.inv(m_INERTIA)	#inverse of inertia matrix
J=np.linalg.eig(m_INERTIA)
Jmin=min(J[0][0],J[0][1],J[0][2])

#Side panel areas
v_Ax = np.array([0.01,0.,0.])	#area vector perpendicular to x-axis in m^2
v_Ay = np.array([0.,0.01,0.])	#area vector perpendicular to y-axis in m^2
v_Az = np.array([0.,0.,0.01])	#area vector perpendicular to z-axis in m^2

#Sunsensor (random values)
v_S1 = np.array([1,0,0])
v_S2 = np.array([-1,0,0])
v_S3 = np.array([0,1,0])
v_S4 = np.array([0,-1,0])
v_S5 = np.array([0,0,1])
v_S6 = np.array([0,0,-1])

SS_GAIN = 1
SS_QUANTIZER = 3
SS_THRESHOLD = 0.5

ADC_BIAS = np.array([0,0,0])
ADC_COV = 0.01*np.identity(3)

#GPS (random values)
GPS_POS_BIAS = np.array([0,0,0])
GPS_VEL_BIAS = np.array([0,0,0])
GPS_TIME_BIAS = 0
GPS_POS_COV = np.identity(3)
GPS_VEL_COV = np.identity(3)
GPS_TIME_COV = 0


#Magnetometer (random values)
MAG_BIAS = np.array([0,0,0])
MAG_COV = 1e-9*np.identity(3)

#------------Initial conditions
v_q0_BO = np.array([1.,0.,0.,0.])	#unit quaternion initial condition

MODEL_STEP=0.1
CONTROL_STEP = 2.0	#control cycle time period in second
h = 0.001 #step size of integration in seconds

INDUCTANCE = 10.7#68e-3	#Inductance of torquer in Henry
RESISTANCE = 107.0	#Resistance of torquer	in Ohm
PWM_AMPLITUDE = 3.3	#PWM amplitude in volt
PWM_FREQUENCY = 1e3 #frequency of PWM signal 
No_Turns=450        #No. of turns of torquer
v_A_Torquer = np.array([0.0049,0.0049,0.0049])	#area vector of torquers in m^2

#Disturbance model constants
SOLAR_PRESSURE = 4.56e-6	#in N/m^2
REFLECTIVITY = 0.2
r_COG_2_COM_b = np.array([-0.69105608e-3,-0.69173140e-3,-2.37203930e-3])
AERO_DRAG = 2.2
RHO = 0.218e-12

k_detumbling = 4*np.pi*(1+sin(radians(Incl_deg-11)))*Jmin/TimePeriod    #gain constant in B_dot controller (from book by F. Landis Markley)