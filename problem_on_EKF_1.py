import numpy as np
import scipy.linalg
import RK4
A1=28
A3=28
A2=32
A4=32
a1=0.071
a3=0.071
a2=0.057
a4=0.057
k_c=0.5
g=981
h1_0=12.0 #initial state
h2_0=12.0 #initial state
h3_0=1.5  #initial state
h4_0=1.0  #initial state
h1_s=12.4 #steady state
h2_s=12.7 #steady state
h3_s=1.8  #steady state
h4_s=1.4  #steady state
v1=3
v2=3
k1=3.33
k2=3.35
gamma1=0.7
gamma2=0.6
Q=[[0.01,0,0],[0,0.01,0],[0,0,0.01]]
random_num = np.random.normal(0,0.01)
C=np.array([[1,0,0,0],[0,1,0,0]])
H=np.identity(4)

def JacobianX(h1,h2,h3,h4):
    A=[[-a1*(np.sqrt(2*g/h1))/(2*A1), 0, a3*(np.sqrt(2*g/h3))/(2*A1), 0],
        [0, -a2*(np.sqrt(2*g/h2))/(2*A2), 0, a4*(np.sqrt(2*g/h4))/(2*A2)],
        [0, 0, -a3*(np.sqrt(2*g/h3))/(2*A3), 0],
        [0, 0, 0, -a4*(np.sqrt(2*g/h4))/(2*A4)]]
    return A

def JacobianU(h1,h2,h3,h4):
    B=np.array([[gamma1*k1/A1,    0],
                [0,    gamma2*k2/A2],
                [0,(1-gamma2)*k2/A3],
                [(1-gamma1)*k1/A4,0]])
    return B    
 
    
def state(h1,h2,h3,h4):
    X=np.array([h1,h2,h3,h4])
    return X

I=np.identity(4)
A=JacobianX(h1_s,h2_s,h3_s,h4_s)
A_inv=np.linalg.inv(A)
B=JacobianU(h1_s,h2_s,h3_s,h4_s)
H=I
U=np.array([v1,v2])
omega = np.linalg.matrix_power(scipy.linalg.expm(A),5)
Tau=np.matmul(np.matmul((omega-I),A_inv),B)

def func_for_true_states(t,X):
    output=np.matmul(A,X) + np.matmul(B,U) #+ np.matmul(H, )
    return output

y0=np.array([h1_0,h2_0,h3_0,h4_0])

true_states=RK4.RK4(func_for_true_states,y0,0,100,0.05)[0]
#print(true_states.T)
psi = np.array([C, np.matmul(C,omega)])
print(psi.shape)







