"""
Creates Fig 2 d+e: Bifurcation diagram for varying fb and fb + fd
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import pandas as pd
from scipy import integrate as integ
import numpy.random as rd 

import savanna_setup as ss

#------------------------------------------------------------------------------------------------------------
#Define helper function to extract necessary data from each simulation:
# ----------------------------------------------------------------------------------------------------------- 

def extract_data(X):
    
    # extract key data
    PH = X[-100:,0]
    PS = X[-100:,1]
    CB = X[-100:,2]
    CG = X[-100:,3]
    
    # append key data to lists 
    shrub_ratio = np.mean(PS)/np.mean(PH + PS)
    browser_ratio = np.mean(CB)/np.mean(CB + CG)
    
    return [min(PH), max(PH), min(PS), max(PS), min(CB), max(CB), min(CG), max(CG), shrub_ratio, browser_ratio]
#----------------------------------------------------------------------------------------------------------------
#Create data for both bifurcation diagrams
#----------------------------------------------------------------------------------------------------------------

# start with list for x-axis
f_list = np.arange(0.0,0.8,0.001)

#initiliase empty lists list to store key data 
data_fb = []
data_fb_fd = []

#make longer time sereis
t_end = 3000 #end of the time series
t_step = 2 #stepsize
t = np.arange(0,t_end,t_step)

#set carrying capacities (used for initial conditions)
KH = 2     # carrying capacity of producer 1 (grasses)   2
KS = 3 

# now loop through f values
for f in f_list:
    
    # for each valus, first choose random initial population densities 
    x0 = [KH/5*rd.random(),KS/2*rd.random(),KS/5*rd.random(),KH/2*rd.random()]
    
    #-------------------------------------------------------------------------------------
    # data for first column - vary only fx:
    fb = f
    fd = 0
    
    # then solve the system numerically
    X= integ.odeint(ss.savannas,x0,t, args = (fb, fd))
    
    data_fb.append(extract_data(X))
    
    #------------------------------------------------------------------------------------
    # now redo the analysis for second column - vary both fx and fc:
    fb = f
    fd = f
    
    # then solve the system numerically
    X= integ.odeint(ss.savannas,x0,t, args = (fb, fd))
    
    data_fb_fd.append(extract_data(X))
    # for each valus, first choose random initial population densities 
    x0 = [KH/5*rd.random(),KS/2*rd.random(),KS/5*rd.random(),KH/2*rd.random()]
    
#turn nested lists into data frames
col_names = ['min_PH', 'max_PH', 'min_PS', 'max_PS', 'min_CB', 'max_CB', 'min_CG', 'max_CG', 'shrub_ratio', 'browser_ratio']
data_fb = pd.DataFrame(data_fb, columns = col_names )
data_fb['f'] = f_list

data_fb_fd = pd.DataFrame(data_fb_fd, columns = col_names)
data_fb_fd['f'] = f_list

#------------------------------------------------------------------------------------------------------------
#Plot 1st diagram: fb is varied, fd = 0
#-------------------------------------------------------------------------------------------------------------

#set font sizes 
title_size = 22
label_size = 24
tick_size = 16

fig = plt.figure(figsize=(12,9))

ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

#subplot1: plants
ax1.plot(data_fb['f'], data_fb['min_PH'], 'g.', label = 'Grasses ($P_H$)')
ax1.plot(data_fb['f'], data_fb['max_PH'], 'g.')
ax1.plot(data_fb['f'], data_fb['min_PS'], 'y.', label = 'Shrubs ($P_S$)')
ax1.plot(data_fb['f'], data_fb['max_PS'], 'y.')
ax1.set_ylim(0.0,3.0)
plt.setp(ax1.get_xticklabels(), fontsize=tick_size)
plt.setp(ax1.get_yticklabels(), fontsize=tick_size)
ax1.legend(fontsize = label_size-1, markerscale = 3 )
ax1.axvline(x=0.35)
ax1.axvline(x=0.50)
ax1.set_ylabel("equilibrium \n population density", fontsize = label_size)


#subplot: herbivores
ax2.plot(data_fb['f'], data_fb['min_CB'], 'r.', label = 'Browsers ($C_B$)')
ax2.plot(data_fb['f'], data_fb['max_CB'], 'r.')
ax2.plot(data_fb['f'], data_fb['min_CG'], 'm.', label = 'Grazers ($C_G$)')
ax2.plot(data_fb['f'], data_fb['max_CG'], 'm.')
plt.setp(ax2.get_xticklabels(), fontsize=tick_size)
plt.setp(ax2.get_yticklabels(), fontsize=tick_size)
ax2.legend(fontsize = label_size-1, markerscale = 3)
ax2.set_ylabel("equilibrium \n population density", fontsize = label_size)
ax2.set_xlabel("farmer support $f_b$, $f_d$ = 0", fontsize = label_size)

#lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
#handles, labels = ax.get_legend_handles_labels()

#ax1.text(-0.13, 3.0, "(d)", fontsize=30)

plt.tight_layout()

fig.savefig("output/Fig2d_Bifurcation_fb.png", dpi = 300)
#---------------------------------------------------------------------------------------------
#Plot 2nd diagram: Both fb and fd are varied
#--------------------------------------------------------------------------------------------

fig = plt.figure(figsize=(12,9))

ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

#subplot1: plants
ax1.plot(data_fb_fd['f'], data_fb_fd['min_PH'], 'g.', label = 'Grasses ($P_H$)')
ax1.plot(data_fb_fd['f'], data_fb_fd['max_PH'], 'g.')
ax1.plot(data_fb_fd['f'], data_fb_fd['min_PS'], 'y.', label = 'Shrubs ($P_S$)')
ax1.plot(data_fb_fd['f'], data_fb_fd['max_PS'], 'y.')
ax1.set_ylim(0.0,3.0)
plt.setp(ax1.get_xticklabels(), fontsize=tick_size)
plt.setp(ax1.get_yticklabels(), fontsize=tick_size)
ax1.legend(loc = 2, fontsize = label_size, markerscale = 3 )
ax1.set_ylabel("equilibrium \n population density", fontsize = label_size)


#subplot: herbivores
ax2.plot(data_fb_fd['f'], data_fb_fd['min_CB'], 'r.', label = 'Browsers ($C_B$)')
ax2.plot(data_fb_fd['f'], data_fb_fd['max_CB'], 'r.')
ax2.plot(data_fb_fd['f'], data_fb_fd['min_CG'], 'm.', label = 'Grazers ($C_G$)')
ax2.plot(data_fb_fd['f'], data_fb_fd['max_CG'], 'm.')
plt.setp(ax2.get_xticklabels(), fontsize=tick_size)
plt.setp(ax2.get_yticklabels(), fontsize=tick_size)
ax2.legend(fontsize = label_size, markerscale = 3)
ax2.set_ylabel("equilibrium \n population density", fontsize = label_size)
ax2.set_xlabel("farmer support $f_b$, $f_d$", fontsize = label_size)

#lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
#handles, labels = ax.get_legend_handles_labels()

#ax1.text(-0.13, 3.0, "(e)", fontsize=26)

plt.tight_layout()

fig.savefig("output/Fig2_Bifurcation_fd_fb.png", dpi = 300)