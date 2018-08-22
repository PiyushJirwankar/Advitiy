import qnv	
import unittest	
import numpy as np
from ddt import ddt,file_data,unpack,data

A=np.array([1,2,3])
B=np.array([-1,-2,-3])
C=np.array([1,-2,-3])
D=np.array([4,-6,7])
E=np.array([0,-3,2])
F=np.array([0,0,0])

q1=np.array([4,1,2,3])
q2=np.array([-4,-1,-2,3])
q3=np.array([4,1,-2,-3])
q4=np.array([-4,-1,2,-3])
q5=np.array([4,-1,-2,-3])
q6=np.array([-4,1,2,-3])
q7=np.array([0,0,2,-3])
q8=np.array([0,0,-2,-3])
q9=np.array([0,0,0,0])

flag=1 # testing for quatInv

G=qnv.quatInv(q1)
if (G == q2).all() == 0:
	flag=0

G=qnv.quatInv(q3)
if (G == q4).all() == 0:
	flag=0

G=qnv.quatInv(q5)
if (G == q6).all() == 0:
	flag=0

G=qnv.quatInv(q7)
if (G == q8).all() == 0:
	flag=0

G=qnv.quatInv(q9)
if (G == q9).all() == 0:
	flag=0

if flag == 1:
	print ("all cases passed for quatInv")
else:
	print ("error for quatInv")
 
###############################################################################
    
#testing for quat2rotm
@ddt
class Testrotmquat(unittest.TestCase):
	@file_data("test-data/test_rot2mquat.json")
	@unpack
	def test_rotm2quat(self,value):
		   
		 
			q = np.asarray(value[3])
			m1 = np.asarray(value[0])
			m2 = np.asarray(value[1])
			m3 = np.asarray(value[2])
			A = np.vstack([m1, m2, m3])
		   
			qo = qnv.rotm2quat(A)  
			self.assertTrue(np.allclose(q,q0))      

if __name__=='__main__':
	unittest.main(verbosity=1)