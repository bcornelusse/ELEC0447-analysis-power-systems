# -*- coding: utf-8 -*-

# Imports
from math import sin, cos, pi
from cmath import exp
import numpy as np
import pandas as pd
import cmath
import math


CASE = 0 # TODO indicate the number of the case that was assigned to you
#0 because statement0. If statement12: CASE = 12

class PowerFlowNR():
    def __init__(self) -> None:
        self.Y = None
        self.J = None        

    def solve(self,tap_pos=0,q_lim=None):
        # Data

        # Per unit bases (3-phase values)
        Pbase = 100  # MVA
        Vbase = 345  # kV
        #TODO Zbase = 
        Zbase = Vbase**2/Pbase

        # Line paramters
        X_km = 0.376    # ohm/km
        R_km = 0.037    # ohm/km

        # Fix the measured and regulated variables, in p.u.
        # E.g. if bus 1 is the slack bus:
        V1_mag = 1.0
        V1_phase = 0
        # TODO for other buses
        V2_mag = 1.05
        P2 = 2 
        P3 = -5
        Q3 = -1

        ## Lines' impedance in p.u., as a function of lines' length ##
        # TODO
        l12_km = np.sqrt(100**2+111.8034**2)
        l31_km = 200
        l23_km = np.sqrt((200-100)**2+111.8034**2)
        Z_12 = (1j*X_km+R_km)*l12_km/Zbase
        Z_43 = (1j*X_km+R_km)*l31_km/Zbase
        Z_23 = (1j*X_km+R_km)*l23_km/Zbase

        Y_12 = 1/Z_12
        print(f"Y_12 = {Y_12}")
        Y_43 = 1/Z_43
        Y_23 = 1/Z_23

        #Impedance associated with transformer
        # Parameters of the transformer, assuming 
        # 1. it has been created in pandapower as 
        # pp.create_transformer_from_parameters(net, b1, b4, name="trfo", sn_mva=1000, vn_hv_kv=Vbase, vn_lv_kv=Vbase, 
        #                               vk_percent=10, vkr_percent=0.3, pfe_kw=0, i0_percent=0, shift_degree=0,
        #                               tap_side="hv", tap_neutral=0, tap_max=9, tap_min=-9, tap_step_percent=0, 
        #                               tap_step_degree=1, tap_pos=0, tap_phase_shifter=True, in_service=True)
        # 2. the power base is 100 MVA for the network
        # 3. the tap position is an integer
        net_sn_mva = 100
        sn_mva = 1000
        vk_percent = 10
        vkr_percent = 0.3
        tap_step_degree = 1

        # Compute the leakage impedance from the data used to specify the transfo (cf. PandaPower documentation):
        z_k = vk_percent / 100 * net_sn_mva / sn_mva
        r_k = vkr_percent / 100 * net_sn_mva / sn_mva
        x_k = math.sqrt(z_k**2 - r_k**2)
        # The values calculated in that way are relative to the rated values of the transformer (cf. https://pandapower.readthedocs.io/en/v2.4.0/elements/trafo.html?highlight=create_transformer_from_parameters#pandapower.create_transformer_from_parameters)
        # I have tryed applying the scaling indicated, it is conterproductive ...

        t = np.exp(1j*(-1)*tap_pos*tap_step_degree*math.pi/180) # Had to multiply by -1 the tap pos to comply with pandapower (???)
        print(f"t = {t}")

        Y_l = 1/(r_k + 1j*x_k)
        print(f"Y_l = {Y_l}")

        ## Admittance matrix as an np.array. 
        
        # Assuming nothing is injected at bus 4, we can simplify the network to buses 1, 2 and 3, by applying the Norton theorem (Cf. Electric circuit course).
        # G_No = G_aa - G_ab * G_bb^{-1} * G_ba
        Y = np.array([[Y_l+Y_12 - Y_l*Y_l/(Y_l+np.abs(t)**2 * Y_43), -Y_12, -Y_l*Y_43*np.conj(t)/(Y_l+np.abs(t)**2 * Y_43)],
                 [-Y_12, Y_12+Y_23, -Y_23],
                 [-Y_l*Y_43*t/(Y_l+np.abs(t)**2 * Y_43), -Y_23, Y_43+Y_23-Y_43*Y_43*np.abs(t)**2/(Y_l+np.abs(t)**2 * Y_43)]])
        # Note: I could have created the 4 by 4 matrix and computed numerically G_No = G_aa - G_ab * G_bb^{-1} * G_ba
        
        G = Y.real  # Conductance matrix
        B = Y.imag  # Susceptance matrix

        # Init Newton-Raphson: set starting values for unknown voltage magnitudes and angles
        V2_phase = 0
        V3_mag = 1
        V3_phase = 0

        def compute_mismatch(q_lim_reached = False):
          # TODO Given the voltage values at the current iteration, estimate the active powers injected at the PV and PQ buses, and the reactive powers injected at PQ buses
            if q_lim_reached:
              # Mismatch vector if the generator's reactive power limit is reached -> PV bus becomes a PQ bus
              # TODO
              P2_est = G[1][1]*V2_mag**2 + V2_mag*(V1_mag*(G[1][0]*cos(V2_phase - V1_phase) + B[1][0]*sin(V2_phase - V1_phase)) + V3_mag*(G[1][2]*cos(V2_phase - V3_phase) + B[1][2]*sin(V2_phase - V3_phase)))
              Q2_est = -B[1][1]*V2_mag**2 + V2_mag*(V1_mag*(G[1][0]*sin(V2_phase - V1_phase) - B[1][0]*cos(V2_phase - V1_phase)) + V3_mag*(G[1][2]*sin(V2_phase - V3_phase) - B[1][2]*cos(V2_phase - V3_phase)))
              P3_est = G[2][2]*V3_mag**2 + V3_mag*(V1_mag*(G[2][0]*cos(V3_phase - V1_phase) + B[2][0]*sin(V3_phase - V1_phase)) + V2_mag*(G[2][1]*cos(V3_phase - V2_phase) + B[2][1]*sin(V3_phase - V2_phase)))
              Q3_est = -B[2][2]*V3_mag**2 + V3_mag*(V1_mag*(G[2][0]*sin(V3_phase - V1_phase) - B[2][0]*cos(V3_phase - V1_phase)) + V2_mag*(G[2][1]*sin(V3_phase - V2_phase) - B[2][1]*cos(V3_phase - V2_phase)))
              # Mismatch: f_exact - f_est
              # TODO return the list of errors between imposed values and evaluated value: mismatch = [...]
              mismatch = [P2-P2_est, Q2-Q2_est, P3-P3_est, Q3-Q3_est]
            else:  
              # Same mismatch vector as the one you've found in programming assignment 1
              # TODO => copy paste from assignment 1
              P2_est = G[1][1]*V2_mag**2 + V2_mag*(V1_mag*(G[1][0]*cos(V2_phase - V1_phase) + B[1][0]*sin(V2_phase - V1_phase)) + V3_mag*(G[1][2]*cos(V2_phase - V3_phase) + B[1][2]*sin(V2_phase - V3_phase)))
              P3_est = G[2][2]*V3_mag**2 + V3_mag*(V1_mag*(G[2][0]*cos(V3_phase - V1_phase) + B[2][0]*sin(V3_phase - V1_phase)) + V2_mag*(G[2][1]*cos(V3_phase - V2_phase) + B[2][1]*sin(V3_phase - V2_phase)))
              Q3_est = -B[2][2]*V3_mag**2 + V3_mag*(V1_mag*(G[2][0]*sin(V3_phase - V1_phase) - B[2][0]*cos(V3_phase - V1_phase)) + V2_mag*(G[2][1]*sin(V3_phase - V2_phase) - B[2][1]*cos(V3_phase - V2_phase)))          
              # Mismatch: f_exact - f_est
              # TODO return the list of errors between imposed values and evaluated value: mismatch = [...]
              mismatch = [P2-P2_est, P3-P3_est, Q3-Q3_est]
            return mismatch

        """Compute the jacobian"""

        def compute_J(q_lim_reached = False):
            ## Jacobian
            if q_lim_reached:
              # Jacobian if the generator's reactive power limit is reached -> PV bus becomes a PQ bus.
              # TODO Initialize with zeros to the right dimensions depending on your problem's size
              # J = np.array([...])
              J = np.array([[0,0,0,0],
                            [0,0,0,0],
                            [0,0,0,0],
                            [0,0,0,0]
              ])

              # TODO Compute each element of the Jacobian
              # J[0][0] = ...
              # J(0,0)=dP2/dtheta2
              J[0][0] = V2_mag*(V1_mag*(-G[1][0]*sin(V2_phase-V1_phase)+B[1][0]*cos(V2_phase-V1_phase)) +
                              V3_mag*(-G[1][2]*sin(V2_phase-V3_phase)+B[1][2]*cos(V2_phase-V3_phase)))
              
              # J(0,1) = dP2/dV2
              J[0][1] = 2*G[1][1]*V2_mag + (V1_mag*(G[1][0]*cos(V2_phase - V1_phase) + B[1][0]*sin(V2_phase - V1_phase)) + 
                                            V3_mag*(G[1][2]*cos(V2_phase - V3_phase) + B[1][2]*sin(V2_phase - V3_phase)))

              # J(0,2)=dP2/dtheta3
              J[0][2] = V2_mag * \
                  (V3_mag*(G[1][2]*sin(V2_phase-V3_phase)-B[1][2]*cos(V2_phase-V3_phase)))

              # J(0,3)=dP2/dV3
              J[0][3] = V2_mag*((G[1][2]*cos(V2_phase-V3_phase) +
                              B[1][2]*sin(V2_phase-V3_phase)))
              
              # J(1,0)=dQ2/dtheta2
              J[1][0] = V2_mag*(V1_mag*(G[1][0]*cos(V2_phase - V1_phase) + B[1][0]*sin(V2_phase - V1_phase)) + 
                                V3_mag*(G[1][2]*cos(V2_phase - V3_phase) + B[1][2]*sin(V2_phase - V3_phase)))
              
              # J(1,1)=dQ2/dV2
              J[1][1] = -2*B[1][1]*V2_mag + (V1_mag*(G[1][0]*sin(V2_phase - V1_phase) - B[1][0]*cos(V2_phase - V1_phase)) + 
                                             V3_mag*(G[1][2]*sin(V2_phase - V3_phase) - B[1][2]*cos(V2_phase - V3_phase)))
              
              # J(1,2)=dQ2/dtheta3
              J[1][2] = V2_mag*(V3_mag*(-G[1][2]*cos(V2_phase - V3_phase) - B[1][2]*sin(V2_phase - V3_phase)))

              # J(1,3)=dQ2/dV3
              J[1][3] = V2_mag*(G[1][2]*sin(V2_phase - V3_phase) - B[1][2]*cos(V2_phase - V3_phase))

              # J(2,0)=dP3/dtheta2
              J[2][0] = V3_mag * \
                  (V2_mag*(G[2][1]*sin(V3_phase-V2_phase)-B[2][1]*cos(V3_phase-V2_phase)))

              # J(2,1)=dP3/dV2
              J[2][1] = V3_mag*(G[2][1]*cos(V3_phase - V2_phase) + B[2][1]*sin(V3_phase - V2_phase))    

              # J(2,2)=dP3/dtheta3
              J[2][2] = V3_mag*(V1_mag*(-G[2][0]*sin(V3_phase-V1_phase)+B[2][0]*cos(V3_phase-V1_phase)) +
                              V2_mag*(-G[2][1]*sin(V3_phase-V2_phase)+B[2][1]*cos(V3_phase-V2_phase)))

              # J(2,3)=dP3/dV3
              J[2][3] = 2*G[2][2]*V3_mag + V1_mag*(G[2][0]*cos(V3_phase-V1_phase)+B[2][0]*sin(
                  V3_phase-V1_phase)) + V2_mag*(G[2][1]*cos(V3_phase-V2_phase)+B[2][1]*sin(V3_phase-V2_phase))

              # J(3,0)=dQ3/dtheta2
              J[3][0] = V3_mag * \
                  (V2_mag*(-G[2][1]*cos(V3_phase-V2_phase)-B[2][1]*sin(V3_phase-V2_phase)))

              # J(3,1)=dQ3/dV2
              J[3][1] = V3_mag*(G[2][1]*sin(V3_phase - V2_phase) - B[2][1]*cos(V3_phase - V2_phase))    

              # J(3,2)=dQ3/dtheta3
              J[3][2] = V3_mag*(V1_mag*(G[2][0]*cos(V3_phase-V1_phase)+B[2][0]*sin(V3_phase-V1_phase)) +
                              V2_mag*(G[2][1]*cos(V3_phase-V2_phase)+B[2][1]*sin(V3_phase-V2_phase)))

              # J(3,3)=dQ3/dV3
              J[3][3] = - 2*B[2][2]*V3_mag + V1_mag*(G[2][0]*sin(V3_phase-V1_phase)-B[2][0]*cos(
                  V3_phase-V1_phase)) + V2_mag*(G[2][1]*sin(V3_phase-V2_phase)-B[2][1]*cos(V3_phase-V2_phase))

            else:
              # Same Jacobian as the one you've found in programming assignment 1
              # TODO => copy paste from assignment 1
              # J = np.array([...])
              J = np.array([[0,0,0],
                            [0,0,0],
                            [0,0,0]
              ])

              # TODO => copy paste from assignment 1
              # J[0][0] = ...
              # J(0,0)=dP2/dtheta2
              J[0][0] = V2_mag*(V1_mag*(-G[1][0]*sin(V2_phase-V1_phase)+B[1][0]*cos(V2_phase-V1_phase)) +
                              V3_mag*(-G[1][2]*sin(V2_phase-V3_phase)+B[1][2]*cos(V2_phase-V3_phase)))
              # J(0,1)=dP2/dtheta3
              J[0][1] = V2_mag * \
                  (V3_mag*(G[1][2]*sin(V2_phase-V3_phase)-B[1][2]*cos(V2_phase-V3_phase)))

              # J(0,2)=dP2/dV3
              J[0][2] = V2_mag*((G[1][2]*cos(V2_phase-V3_phase) +
                              B[1][2]*sin(V2_phase-V3_phase)))

              # J(1,0)=dP3/dtheta2
              J[1][0] = V3_mag * \
                  (V2_mag*(G[2][1]*sin(V3_phase-V2_phase)-B[2][1]*cos(V3_phase-V2_phase)))

              # J(1,1)=dP3/dtheta3
              J[1][1] = V3_mag*(V1_mag*(-G[2][0]*sin(V3_phase-V1_phase)+B[2][0]*cos(V3_phase-V1_phase)) +
                              V2_mag*(-G[2][1]*sin(V3_phase-V2_phase)+B[2][1]*cos(V3_phase-V2_phase)))

              # J(1,2)=dP3/dV3
              J[1][2] = 2*G[2][2]*V3_mag + V1_mag*(G[2][0]*cos(V3_phase-V1_phase)+B[2][0]*sin(
                  V3_phase-V1_phase)) + V2_mag*(G[2][1]*cos(V3_phase-V2_phase)+B[2][1]*sin(V3_phase-V2_phase))

              # J(2,0)=dQ3/dtheta2
              J[2][0] = V3_mag * \
                  (V2_mag*(-G[2][1]*cos(V3_phase-V2_phase)-B[2][1]*sin(V3_phase-V2_phase)))

              # J(2,1)=dQ3/dtheta3
              J[2][1] = V3_mag*(V1_mag*(G[2][0]*cos(V3_phase-V1_phase)+B[2][0]*sin(V3_phase-V1_phase)) +
                              V2_mag*(G[2][1]*cos(V3_phase-V2_phase)+B[2][1]*sin(V3_phase-V2_phase)))

              # J(2,2)=dQ3/dV3
              J[2][2] = - 2*B[2][2]*V3_mag + V1_mag*(G[2][0]*sin(V3_phase-V1_phase)-B[2][0]*cos(
                  V3_phase-V1_phase)) + V2_mag*(G[2][1]*sin(V3_phase-V2_phase)-B[2][1]*cos(V3_phase-V2_phase))

            return J

        def solve_linear_system(J, mismatch):
            # Solve Ax = b where A is J and b is the mismatch, nothing to do for you here
            deltas = np.linalg.solve(J, mismatch)
            return deltas


        def update_V(V2_phase, V3_phase, V3_mag, deltas, V2_mag = 0, q_lim_reached = False):
            """Update the unknown values (V and theta for PQ buses and theta for PV buses)"""
            # Update the approximated solutions
            if q_lim_reached:
              # TODO if the generator's reactive power limit is reached -> PV bus becomes a PQ bus.
              V2_phase = V2_phase + deltas[0]
              V2_mag = V2_mag + deltas[1]
              V3_phase = V3_phase + deltas[2]
              V3_mag = V3_mag + deltas[3]   
              return V2_phase,V2_mag,V3_phase,V3_mag#TODO
            else:
              # Same as programming assignment 1
              # TODO same update vector as the one you've found in programming assignment 1
              V2_phase = V2_phase + deltas[0]
              V3_phase = V3_phase + deltas[1]
              V3_mag = V3_mag + deltas[2]            
              return V2_phase,V3_phase,V3_mag# TODO

########################### FIRST STEP#######################################################
       
        # Solve the power flow and check if the reactive power limit has been overreached              

        # Algorithm parameters
        n_iter = 0 # Number of iterations, will be incremented
        convergence_flag = False # Flag that will be set to True after convergence
        tol = 1e-4 # Tolerance on the injections - you may have to change this to pass the tests, or not...

        # Start the solution process
        while(not convergence_flag):
            mismatch = compute_mismatch()
            if max(map(abs, mismatch)) < tol: # Are all the residuals below the tolerance? 
                convergence_flag = True
            J = compute_J()
            # for test purpose
            self.J = np.multiply(J,float(Pbase))
            deltas = solve_linear_system(J, mismatch)
            # TODO Update the voltages using the deltas
            V2_phase, V3_phase, V3_mag = update_V(V2_phase, V3_phase, V3_mag, deltas)            
            # TODO You may want to print how things evolve over the iterations 
            print("Iteration %d: P2_exact - P2_est = %.8f, P3_exact - P3_est = %.8f, Q3_exact - Q3_est = %.8f" %
                (n_iter, mismatch[0], mismatch[1], mismatch[2]))            
            n_iter += 1

        # Compute the unknown power injections (at slack bus and PV buses)
        # TODO 
        P1 = G[0][0]*V1_mag**2 + V1_mag*(V2_mag*(G[0][1]*cos(V1_phase - V2_phase) + B[0][1]*sin(V1_phase - V2_phase)) + V3_mag*(G[0][2]*cos(V1_phase - V3_phase) + B[0][2]*sin(V1_phase - V3_phase)))
        Q1 = -B[0][0]*V1_mag**2 + V1_mag*(V2_mag*(G[0][1]*sin(V1_phase - V2_phase) - B[0][1]*cos(V1_phase - V2_phase)) + V3_mag*(G[0][2]*sin(V1_phase - V3_phase) - B[0][2]*cos(V1_phase - V3_phase)))
        Q2 = -B[1][1]*V2_mag**2 + V2_mag*(V1_mag*(G[1][0]*sin(V2_phase - V1_phase) - B[1][0]*cos(V2_phase - V1_phase)) + V3_mag*(G[1][2]*sin(V2_phase - V3_phase) - B[1][2]*cos(V2_phase - V3_phase)))

########################### SECOND STEP#######################################################

        #Check if the reactive power limit has been overreached. If the answer is yes, 
        #change the PV bus in a PQ bus and solve the power flow again.
        if not q_lim:
            q_lim=1e10

        if abs(Q2)>abs(q_lim/Pbase): #TODO
          print('Q limit has been reached')
          #Impose the reactive power of the PQ bus to q_lim
          # TODO          
          Q2 = q_lim/Pbase
          # Init Newton-Raphson: set starting values for unknown voltage magnitudes and angles
          # TODO
          V2_phase = 0
          V2_mag = 1
          V3_mag = 1
          V3_phase = 0
          # Algorithm parameters
          n_iter = 0 # Number of iterations, will be incremented
          convergence_flag = False # Flag that will be set to True after convergence
          tol = 1e-4 # Tolerance on the injections - you may have to change this to pass the tests, or not...          
          # Start the solution process
          while(not convergence_flag):
              mismatch = compute_mismatch(q_lim_reached = True)
              if max(map(abs, mismatch)) < tol: # Are all the residuals below the tolerance? 
                  convergence_flag = True
              J = compute_J(q_lim_reached = True)
              # for test purpose
              self.J = np.multiply(J,float(Pbase))
              deltas = solve_linear_system(J, mismatch)
              # TODO Update the voltages using the deltas
              V2_phase, V2_mag, V3_phase, V3_mag = update_V(V2_phase, V3_phase, V3_mag, deltas, V2_mag = V2_mag, q_lim_reached = True)            
              # TODO You may want to print how things evolve over the iterations 
              print("Iteration %d: P2_exact - P2_est = %.8f, Q2_exact - Q2_est = %.8f, P3_exact - P3_est = %.8f, Q3_exact - Q3_est = %.8f" %
                  (n_iter, mismatch[0], mismatch[1], mismatch[2], mismatch[3]))            
              n_iter += 1      
          # Compute the unknown power injections (at slack bus)
          # TODO 
          P1 = G[0][0]*V1_mag**2 + V1_mag*(V2_mag*(G[0][1]*cos(V1_phase - V2_phase) + B[0][1]*sin(V1_phase - V2_phase)) + V3_mag*(G[0][2]*cos(V1_phase - V3_phase) + B[0][2]*sin(V1_phase - V3_phase)))
          Q1 = -B[0][0]*V1_mag**2 + V1_mag*(V2_mag*(G[0][1]*sin(V1_phase - V2_phase) - B[0][1]*cos(V1_phase - V2_phase)) + V3_mag*(G[0][2]*sin(V1_phase - V3_phase) - B[0][2]*cos(V1_phase - V3_phase)))


        # Return the solution in a format equivalent to pandapowers output
        solution_array= [[V1_mag, V1_phase*180/pi, -P1*Pbase, -Q1*Pbase],
                         [V2_mag, V2_phase*180/pi, -P2*Pbase, -Q2*Pbase],
                         [V3_mag, V3_phase*180/pi, -P3*Pbase, -Q3*Pbase]]

        col_names=["vm_pu", "va_degree", "p_mw","q_mvar"]
        res_bus = pd.DataFrame(solution_array, columns=col_names)

        return res_bus

if __name__=='__main__':
    pfcalculator = PowerFlowNR()
    # check if everything is ok by playing with the value of tap_pos and q_lim    
    student_res_bus = pfcalculator.solve(tap_pos=-4,q_lim=500)
    print(student_res_bus)