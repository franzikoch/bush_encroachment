"""
Creates Fig3 timeseries with transitions between states
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import pandas as pd
from scipy import integrate as integ
import numpy.random as rd 

import savanna_setup as ss

#---------------------------------------------------------------------------------------------------
#Define function to simulate disturbances
#--------------------------------------------------------------------------------------------------

def simulate_droughts(sections_number, season_length, N0 , f_values, d_values, introduce_browsers):
    
    """
    Splits the simulation in a number of sections, that are seperated by drought events that kill d% of grasses ans d/5 % of shrubs
    f can be varied for each section
    """
    
    #check if f_values, d_values and introduce_browsers have n = section number entries
    if len(f_values)!= sections_number: print("Incorrect number of f values")
    if len(d_values)!= sections_number: print("Incorrect number of d values")                                   
    if len(introduce_browsers)!= sections_number: print("Incorrect number of introduce browsers")
   
    #prepare timesteps array for one section of the time series
    time = np.arange(0, season_length)

    #prepare matrices to store results
    #N will contain the results for all populations at each timestep
    num_rows = sections_number*(len(time))+sections_number+1 #number of rows that N needs to have to store everything

    N = np.zeros([num_rows, 4])
    N[0,:] = N0

    count = 0 #counts how many growing seasons have been completed
    t = 1 # used to index N/counting all time steps

    #define extinction threshold
    epsilon = 0.00001

    while count < sections_number :

        x0 = N[t-1, :]
         
        fb = f_values[count]
        
        X = integ.odeint(ss.savannas, x0, time, args = (fb,fd))
        
        #put X into N
        N[t:t+len(time), :] = X

        #update index
        t = t+len(time)
        
        ##DROUGHT!
        #calculate the amount of biomass that survives
        PH = X[-1,0]*(1-d_values[count])
        PS = X[-1,1]*(1-0.2*d_values[count])
        C1 = X[-1,2]
        C2 = X[-1,3]
        
        ##Reintroduction of BROWSERS!
        if (C1< epsilon and introduce_browsers[count] == True):
            #reintroduce a small number of browsers to the system
            C1 = 0.01
            
        #define new N for t
        N[t,:] = np.array([PH, PS, C1,C2])

        #update index and counter
        count = count + 1
        t = t+1
    
    return N


#general setup :   

#define time array for simulations
t_end = 1000 #end of the time series
t_step = 1 #stepsize
t = np.arange(0,t_end,t_step)

fd = 0 #only fb is varied here

#set carrying capacities (used for initial conditions)
KH = 2     # carrying capacity of producer 1 (grasses)   2
KS = 3  

#set font sizes for plots  
title_size = 22
label_size = 22
tick_size = 16
#--------------------------------------------------------------------------------------
#Fig 3a: Moderate increase of farmer support
#-------------------------------------------------------------------------------------

sections_number = 6  #number of disturbances
season_length = 1000 #number timesteps between droughts

N0 = [KH/2*rd.random(),KS/10*rd.random(),KH/5*rd.random(),KS/2*rd.random()] #initial population densities

#each value in the list describes what happens at the end of the corresponding section
f_values = [0, 0, 0.35, 0.35, 0, 0]
d_values = [0.95, 0, 0.95, 0, 0, 0]
introduce_browsers = [0,0,0,0,1,0]

N_total = simulate_droughts(sections_number, season_length, N0, f_values, d_values, introduce_browsers)
N_total = pd.DataFrame(N_total, columns = ['PH', 'PS', 'CB', 'CG'])
N_total['time'] = np.arange(N_total.shape[0])

#plotting
fig = plt.figure(figsize=(15,5))

plt.plot(N_total['time'], N_total['PH'],"g",  label = "Grasses ($P_H$)", linewidth = 2)
plt.plot(N_total['time'], N_total['PS'], "y", label = "Shrubs ($P_S$)", linewidth = 2)
plt.plot(N_total['time'], N_total['CB'], "r", label = "Browsers ($C_B$)", linewidth = 2)
plt.plot(N_total['time'], N_total['CG'], "m", label = "Grazers ($C_G$)", linewidth = 2)

plt.ylim(0.0,3.5)
#plt.xlim(0, 6000)
plt.legend(bbox_to_anchor=(1.02, 0.7), loc=2, borderaxespad=0., fontsize = label_size)
plt.yticks(fontsize = tick_size)
plt.xticks(fontsize = tick_size)
plt.xlabel("Time t", fontsize = label_size)
plt.ylabel("Population density", fontsize = label_size)

# add arrows and labels:
#ax = plt.axes()
arrow_placement = 2.7
text_placement = 2.85
plt.annotate('', xy=(0,arrow_placement),
            xytext=(2000,arrow_placement), va='center', multialignment='center',
            arrowprops={'arrowstyle': '<|-|>', 'lw': 3, 'ec': 'k'})
plt.text(300, text_placement, 'no farmer support \n        ($f_{b}=0$)', fontsize = label_size)

plt.annotate('', xy=(2000,arrow_placement),
            xytext=(4000,arrow_placement), va='center', multialignment='center',
            arrowprops={'arrowstyle': '<|-|>', 'lw': 3, 'ec': 'k'})
plt.text(2020, text_placement, 'increased farmer support\n          ($f_{b}=0.35$)', fontsize = label_size)

plt.annotate('', xy=(4000, arrow_placement),
            xytext=(6000,arrow_placement), va='center', multialignment='center',
            arrowprops={'arrowstyle': '<|-|>', 'lw': 3, 'ec': 'k'})
plt.text(4300, text_placement, 'no farmer support \n     ($f_{b}=0)$', fontsize = label_size)

plt.text(950, 2.3, r'*', fontsize='25')
plt.text(2950, 2.3, r'*', fontsize='25');
plt.text(4950, 2.3, r'$^\bigtriangledown$', fontsize='25')

#add panel identifier
#plt.text(-1000, 3.6, "(A)", fontsize=26)
plt.savefig("output/Fig3a_timeseries1.pdf", dpi = 150, bbox_inches='tight')

#---------------------------------------------------------------------------------------------
#Fig 3B: Strong increase in farmer support
#------------------------------------------------------------------------------------------
sections_number = 6  #number of disturbances
season_length = 1000 #number timesteps between droughts

N0 = [KH/2*rd.random(),KS/10*rd.random(),KH/5*rd.random(),KS/2*rd.random()] #initial population densities

#each value in the list describes what happens at the end of the corresponding section
f_values = [0, 0, 0.5, 0.5, 0, 0]
d_values = [0.95, 0, 0.95, 0, 0, 0]
introduce_browsers = [0,0,0,0,1,0]

N_total = simulate_droughts(sections_number, season_length, N0, f_values, d_values, introduce_browsers)
N_total = pd.DataFrame(N_total, columns = ['PH', 'PS', 'CB', 'CG'])
N_total['time'] = np.arange(N_total.shape[0])

#plotting
fig = plt.figure(figsize=(15,5))

plt.plot(N_total['time'], N_total['PH'],"g", label = "Grasses ($P_H$)", linewidth = 2)
plt.plot(N_total['time'], N_total['PS'], "y",  label = "Shrubs ($P_S$)",  linewidth = 2)
plt.plot(N_total['time'], N_total['CB'], "r", label = "Browsers ($C_B$)",  linewidth = 2)
plt.plot(N_total['time'], N_total['CG'], "m", label = "Grazers ($C_G$)",  linewidth = 2)

plt.ylim(0.0,3.5)
plt.legend(bbox_to_anchor=(1.02, 0.7), loc=2, borderaxespad=0., fontsize = label_size)

plt.xlabel("Time t", fontsize = label_size)
plt.ylabel("Population density", fontsize = label_size)

plt.yticks(fontsize = tick_size)
plt.xticks(fontsize = tick_size)

# add arrows and labels:
#ax = plt.axes()
plt.annotate('', xy=(0,arrow_placement),
            xytext=(2000,arrow_placement), va='center', multialignment='center',
            arrowprops={'arrowstyle': '<|-|>', 'lw': 3, 'ec': 'k'})
plt.text(300, text_placement, 'no farmer support \n        ($f_{b}=0$)', fontsize = label_size)

plt.annotate('', xy=(2000,arrow_placement),
            xytext=(4000,arrow_placement), va='center', multialignment='center',
            arrowprops={'arrowstyle': '<|-|>', 'lw': 3, 'ec': 'k'})
plt.text(2020, text_placement, 'increased farmer support\n          ($f_{b}=0.5$)', fontsize = label_size)

plt.annotate('', xy=(4000, arrow_placement),
            xytext=(6000,arrow_placement), va='center', multialignment='center',
            arrowprops={'arrowstyle': '<|-|>', 'lw': 3, 'ec': 'k'})
plt.text(4300, text_placement, 'no farmer support \n     ($f_{b}=0)$', fontsize = label_size)


plt.text(950, 2.3, r'*', fontsize='25')
plt.text(2950, 2.3, r'*', fontsize='25')
plt.text(4950, 2.3, r'$^\bigtriangledown$', fontsize='25')

#add oanel identifier
#plt.text(-1000, 3.6, "(b)", fontsize=26)

plt.savefig("output/Fig3b_timeseries2.pdf", dpi = 150, bbox_inches='tight')