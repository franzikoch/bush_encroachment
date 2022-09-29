"""
Creates Fig. 2 a-c: Visualising the bistable region with heatmaps
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

from scipy import integrate as integ
import numpy.random as rd 

import savanna_setup as ss

#----------------------------------------------------------------------------------------------------------
#Create data for heatmaps 
#----------------------------------------------------------------------------------------------------------

#define time array for simulation 
t_end = 1000 #end of the time series
t_step = 1 #stepsize
t = np.arange(0,t_end,t_step)

#set carrying capacities (used for initial conditions)
KH = 2     # carrying capacity of producer 1 (grasses)   2
KS = 3 

#set extinction threshold
epsilon = 0.00001

num_vals = 40                                   # number of values on the x- and y-axis
fb_vals = np.linspace(0.0,0.8,num_vals)         # farmer support (reduce mortality) - columns
fd_vals = np.linspace(0.0,0.8,num_vals)         # farmer support (reduce density dependent loss) - rows
shrub_ratio = np.zeros((num_vals,num_vals))     # empty matrix, containing only zeros
browser_ratio = np.zeros((num_vals,num_vals))   # another empty matrix, containing only zeros
survivors = np.zeros((num_vals,num_vals))       # a third matrix containing only zeros

for i in range(num_vals):                       # loop through row valus
    for j in range(num_vals):                   # loop through column valus
                
        fd = fd_vals[i]
        fb = fb_vals[j]
            
        # for each combination of fc and fx, first choose random initial population densities 
        x0 = [KH/2*rd.random(),KS*rd.random(),KS/5*rd.random(),KH/2*rd.random()]
                
        # then solve the system numerically
        X= integ.odeint(ss.savannas,x0,t, args = (fb, fd))          
            
        # extract stationary part of the time series
        PH = X[-300:,0]
        PS = X[-300:,1]
        CB = X[-300:,2]
        CG = X[-300:,3]
        
        if PH[-1]>epsilon:
            survivors[i,j] = survivors[i,j] +1
        if PS[-1]>epsilon:
            survivors[i,j] = survivors[i,j] +1
        if CB[-1]>epsilon:
            survivors[i,j] = survivors[i,j] +1
        if CG[-1]>epsilon:
            survivors[i,j] = survivors[i,j] +1

        # calculate shrub ratio and browser ratio
        shrub_ratio[i,j] = np.mean(PS)/np.mean(PH + PS)
        browser_ratio[i,j]=  np.mean(CB)/np.mean(CB + CG)
    

#---------------------------------------------------------------------------------------------------
#Plot heatmaps
#--------------------------------------------------------------------------------------------------
fig = plt.figure(figsize=(18,5), constrained_layout = True)

#set font sizes 
title_size = 22
label_size = 20
tick_size = 16

#initialise subplots 
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

#first heatmap: shrub ratio
im = ax1.pcolor(fb_vals,fd_vals,shrub_ratio,vmin=0, vmax=1)             
ax1.set_title("ratio of shrubs within total \n plant population", fontsize = title_size)
ax1.set_xlabel('farmer support $f_{b}$', fontsize = label_size)
ax1.set_ylabel('farmer support $f_{d}$', fontsize = label_size);
plt.setp(ax1.get_xticklabels(), fontsize=tick_size)
plt.setp(ax1.get_yticklabels(), fontsize=tick_size)
cbar = plt.colorbar(im, ax = ax1)
cbar.ax.tick_params(labelsize = tick_size)
ax1.text(-0.15, 0.88, "(a)", fontsize=26)

#second heatmap: browser ratio
im = ax2.pcolor(fb_vals,fd_vals,browser_ratio,vmin=0, vmax=0.5)             
ax2.set_title("ratio of browsers within total \n animal population", fontsize = title_size)
ax2.set_xlabel('farmer support $f_{b}$', fontsize = label_size)
ax2.set_ylabel('farmer support $f_{d}$', fontsize = label_size);
plt.setp(ax2.get_xticklabels(), fontsize=tick_size)
plt.setp(ax2.get_yticklabels(), fontsize=tick_size)
cbar = plt.colorbar(im, ax = ax2)
cbar.ax.tick_params(labelsize = tick_size)
ax2.text(-0.18, 0.88, "(b)", fontsize=26)

#create discrete colorbar
my_cmap = plt.get_cmap("viridis", 3) 
norm = colors.BoundaryNorm(boundaries = [2, 3, 4], ncolors = 3)

#third heatmap: number of surviving populations
im = ax3.pcolor(fb_vals,fd_vals,survivors.astype(int), cmap = my_cmap)              
ax3.set_title("number of coexisting populations \n within the food web module", fontsize = title_size)
ax3.set_xlabel('farmer support $f_{b}$', fontsize = label_size)
ax3.set_ylabel('farmer support $f_{d}$', fontsize = label_size);
plt.setp(ax3.get_xticklabels(), fontsize=tick_size)
plt.setp(ax3.get_yticklabels(), fontsize=tick_size)
cbar = plt.colorbar(im, ax = ax3, norm = norm, ticks = [2,3,4])
cbar.ax.tick_params(labelsize = tick_size)

ax3.text(-0.25, 0.88, "(c)", fontsize=26)

#plt.tight_layout()

fig.savefig("output/Fig2_heatmaps.pdf", dpi = 150)
plt.close()