"""
Creates Fig 4: Resistance to external disturbances in dependence of the level of farmer support to
reduce grazer mortality ( fb).
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

from scipy import integrate as integ
import numpy.random as rd 

import savanna_setup as ss


#--------------------------------------------------------------------------------------------------
#Create data for heatmap
#--------------------------------------------------------------------------------------------------


#set carrying capacities (used for initial conditions)
KH = 2     # carrying capacity of producer 1 (grasses)   2
KS = 3 

#define time array for simulations
t_end = 1000 #end of the time series
t_step = 1 #stepsize
t = np.arange(0,t_end,t_step)

x0 = [KH/2*rd.random(),KS/5*rd.random(),KH/5*rd.random(),KS/2*rd.random()]

#create reference scenario
fb = 0.3
fd = 0
reference = integ.odeint(ss.savannas,x0,t, args = (fb, fd))   # end point of this time series are used as starting points below


num_vals = 40                                        # number of values on the x- and y-axis
f_vals = np.linspace(0.0,0.8,num_vals)               # farmer investment (reduce background mortality) - columns
disturbance_vals = np.linspace(50,99,num_vals)      # severity of droughts - rows

#initialise empty matrices to fill
shrub_ratio_new = np.zeros((num_vals,num_vals))      # empty matrix, containing only zeros
browser_ratio_new = np.zeros((num_vals,num_vals))    # another empty matrix, containing only zeros
grazer_absolute_new = np.zeros((num_vals,num_vals))  # a third empty matrix, containing only zeros

for i in range(num_vals):                       # loop through row valus -> disturbance
    for j in range(num_vals):                   # loop through column values -> farmer support fb
        

        disturbance = disturbance_vals[i]      
        fb = f_vals[j]
            
        # for each combination of parameter values, first choose random initial population densities 
        x0 = [reference[-1,0], reference[-1,1], reference[-1,2], reference[-1,3]]
        
        # then let the system run for a while to reach an attractor
        X0 = integ.odeint(ss.savannas,x0,t, args = (fb, fd))

        PH_0 = X0[:,0]
        PS_0 = X0[:,1]
        CB_0 = X0[:,2]
        CG_0 = X0[:,3]
        
        # then perform disturbance and let the system run for another while
        # disturbance level of d means that the drought kills d% of grass biomass and d/5% of shrub biomass
        x0_new = [PH_0[-1]*(1-disturbance/100), PS_0[-1]*(1-disturbance/(5*100)), CB_0[-1], CG_0[-2]]   # new initial population densities
        X1 = integ.odeint(ss.savannas,x0_new,t, args = (fb, fd))

        # extract stationary part of the time series
        PH_1 = X1[-300:,0]
        PS_1 = X1[-300:,1]
        CB_1 = X1[-300:,2]
        CG_1 = X1[-300:,3]

        # calculate shrub ratio and browser ratio
        shrub_ratio_new[i,j] = np.mean(PS_1)/np.mean(PH_1 + PS_1)
        browser_ratio_new[i,j] = np.mean(CB_1)/np.mean(CB_1 + CG_1)
        grazer_absolute_new[i,j] = np.mean(CG_1)
        
#-------------------------------------------------------------------------------------------------
#Plot heatmaps
#-----------------------------------------------------------------------------------------------
#set font sizes 
title_size = 22
label_size = 20
tick_size = 16

fig = plt.figure(figsize=(18,5), constrained_layout = True)

#1. Heatmap: Shrub ratio
plt.subplot2grid((1,3), (0,0))
plt.pcolor(f_vals,disturbance_vals,shrub_ratio_new,vmin=0, vmax=1)            

plt.title("ratio of shrubs within total \n plant population AFTER drought", fontsize = title_size)
plt.xlabel('farmer support $f_{b}$', fontsize = label_size)
plt.ylabel('severity of drought $d$', fontsize = label_size);
plt.yticks(fontsize = tick_size)
plt.xticks(fontsize = tick_size)
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize = tick_size)
plt.text(-0.15, 105, "(a)", fontsize=26)

#2. Heatmap: Browser ratio
plt.subplot2grid((1,3), (0,1))
plt.pcolor(f_vals,disturbance_vals,browser_ratio_new,vmin=0, vmax=0.5)             
plt.title("ratio of browsers within total \n animal population AFTER drought", fontsize = title_size)
plt.xlabel('farmer support $f_{b}$', fontsize = label_size)
plt.ylabel('severity of drought $d$', fontsize = label_size);
plt.yticks(fontsize = tick_size)
plt.xticks(fontsize = tick_size)
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize = tick_size)
plt.text(-0.2, 105, "(b)", fontsize=26)

#3. Heatmap: grazer density
plt.subplot2grid((1,3), (0,2))
plt.pcolor(f_vals,disturbance_vals,grazer_absolute_new,vmin=0.6, vmax=1.8)              
plt.title("population density of grazers \n AFTER drought", fontsize = title_size)
plt.xlabel('farmer support $f_{b}$', fontsize = label_size)
plt.ylabel('severity of drought $d$', fontsize = label_size);
plt.yticks(fontsize = tick_size)
plt.xticks(fontsize = tick_size)
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize = tick_size)
plt.text(-0.2, 105, "(c)", fontsize=26)

#plt.tight_layout() 

fig.savefig("output/Fig4_heatmap_drought_resistance.png", dpi = 300)