import numpy as np

def rk4_w_BO_b(sat, f, h):
    
    v_state_w_BO_b_0 = sat.getState()[4:7]	#state at t = t0	
	t = sat.getTime() 
	#rk-4 routine (updating satellite class state with obtained state at every step of rk4 routine)
	#first step of rk4 routine
	k1 = h*f(sat)

	#second step of rk4 routine
	v_state_error_1 = v_state_error_0 + 0.5*k1
	sat.setState(v_state_error_1)

	k2 = h*f(sat)

	#third step of rk4 routine	
	v_state_error_2 = v_state_error_0+0.5*k2
	sat.setState(v_state_error_2)

	k3 = h*f(sat)
	v_state_error_3 = v_state_error_0+k3
	sat.setState(v_state_error_3)

	#forth step of rk4 routine
	k4 = h*f(sat)
	v_state_error_new = v_state_error_0 + (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)

	sat.setState(v_state_error_new.copy())
	print(sat.getState())

	return 