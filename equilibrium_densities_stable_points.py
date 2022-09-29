"""
Estimates equilibrium densities of the stable fixed points from numerical simulations

Input:
unstable_fixed_points.csv -> equilibrium densities of the unstable point, found with XPP Auto.
Is used to get the same fb-values for the unstable point.

Output: table of equilibrium densities.
grassy_states_densities.csv
encroached_states_densities.csv

"""

import numpy as np
from scipy import integrate as integ
import random as rd
import pandas as pd

#--------------------------------------------------------------------
#Preparations
#--------------------------------------------------------------------

#define all parameter values
#------------------------------------------------------------------
rH = 1.0   # intrinsic growth rate of producer 1 (grasses)    1.0
rS = 0.5   # intrinsic growth rate of producer 2 (shrubs)     0.5

KH = 2     # carrying capacity of producer 1 (grasses)   2
KS = 3     # carrying capacity of producer 2 (shrubs)     3

c = 0.3    # interspecific competition - shrubs affect grasses   0.2   or 0.3

mb = 0.15   # consumer background mortality rate         0.15
md = 0.05    # consumer density-dependent mortality rate     0.05

fb = 0.0  # farmer support (reduce background mortality & respiration loss rate)
fd = 0.0  # farmer support (reduce density dependent mortality)

e = 0.45   # conversion efficiency
a = 1      # attack rate
h = 3      # handling time

epsilon = 0.00001  # extinction threshold

#preferences
pHB = 0.3    # browser preference for grasses
pSB = 1- pHB # browser preference for shrubs

pHG = 0.7    # grazer preference for grasses
pSG = 1- pHG # grazer preference for shrubs

#define for how many time steps the simulation is run
t_end = 1000 #end of the time series
t_step = 1 #stepsize
t = np.arange(0,t_end,t_step)

#define the system of equations
#--------------------------------------------------------------
def savannas(x, t, fb, fd, threshold = epsilon):
    
        PH = x[0]  #Producer 1 -> grasses
        PS = x[1]  #Producer 2 -> shrubs
        CB = x[2]  #Consumer 1 -> browsers 
        CG = x[3]  #Consumer 2 -> grazers 

        #Functional responses 
        FHB = (a * PH * pHB)/(1 + a * h * PH * pHB)      #browsers eating grasses
        FHG = (a * PH * pHG)/(1 + a * h * PH * pHG)      #grazers eating grasses
        FSB = (a * PS * pSB)/(1 + a * h * PS * pSB)      #browsers eating shrubs
        FSG = (a * PS * pSG)/(1 + a * h * PS * pSG)      #grazers eating shrubs 
        
        #Differential Equations
                
        #if conditions are used to mimick an extinction threshold
        if PH < threshold:
            dPH_dt = 0
        else:
            dPH_dt = rH * PH * (1-((PH + c*PS) /KH))- FHB*CB - FHG*CG  # grasses
            
        if PS < threshold:
            dPS_dt = 0   
        else:
            dPS_dt = rS * PS * (1-((PS + c*PH) /KS))- FSB*CB - FSG*CG   # shrubs

        if CB < threshold:
            dCB_dt = 0
        else:
            dCB_dt = e*(FHB+FSB)*CB - mb*CB - md*CB*CB        # browser
        
        if CG < threshold:
            dCG_dt = 0
        else:
            dCG_dt = e*(FHG+FSG)*CG - mb*(1-fb)*CG - md*(1-fd)*CG*CG  # grazer
    
        return [dPH_dt, dPS_dt, dCB_dt, dCG_dt]
#-------------------------------------------------------------------------
#get f-values from the unstable fixed_points file
unstable_points = pd.read_csv("unstable_fixed_points.csv")
f_values = np.array(unstable_points['fb'])

encroached_states = [] 
grassy_states = []

n_states = 0 #counts how many stable states have been found

for f in f_values: 
    
    encroached_state = []
    grassy_state = []
    
    #repeatedly run the simulation with random inital conditions to get both fixed points:    
    while not encroached_state or not grassy_state: 
        #while loop is repeated until both lists are not empty anymore
         
        # for each valus, first choose random initial population densities 
        x0 = [KH/5*rd.random(),KS/2*rd.random(),KS/5*rd.random(),KH/2*rd.random()]
    
        #-------------------------------------------------------------------------------------
        # data for first column - vary only fx:
        fb = f
        fd = 0
        
        #print(fb)
        
        # then solve the system numerically
        X= integ.odeint(savannas,x0,t, args = (fb, fd))
        
        #extract equilibrium densities:
        PH = float(X[-1:,0])
        PS = float(X[-1:,1])
        CB = float(X[-1:,2])
        CG = float(X[-1:,3])
        
        #check whether we are in the encroached state or not
        #fill out list if it is empty
        if PS > 1.3 and not encroached_state:
            encroached_state = ([PH, PS, CB, CG])
        elif PS < 1.3 and not grassy_state:
            grassy_state = ([PH, PS, CB, CG])
            
    #print results
    print("fb = ", f)
    print("encroached state:" , encroached_state)
    print("grassy state: ", grassy_state)
    
    #add data to list
    grassy_states.append(grassy_state)
    encroached_states.append(encroached_state)

#turn lists into a dataframe
col_names = ["PH", "PS", "CB", "CG"]

grassy_states = pd.DataFrame(grassy_states, columns = col_names)
encroached_states = pd.DataFrame(encroached_states, columns = col_names)

#add columns with f values
grassy_states["fb"] = f_values
encroached_states["fb"] = f_values

grassy_states.to_csv("grassy_states_densities.csv")
encroached_states.to_csv("encroached_states_densities.csv")
