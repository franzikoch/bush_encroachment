"""
Creates Fig 1b) Two example time series 
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate as integ


import savanna_setup as ss
#-------------------------------------------------------------
#Set farmer investment values 

fb = 0.35  # farmer investment 1
fd = 0.0  # farmer investment 2

#define time array for simulation 
t_end = 1000 #end of the time series
t_step = 1 #stepsize
t = np.arange(0,t_end,t_step)


#--------------------------------------------------------------
# first time series:
x0 = [1.0, 0.2, 0.5, 0.1]        # initial population densities
X= integ.odeint(ss.savannas,x0,t, args = (fb, fd))   # integrate the system
XP1 = X[:,0]                     # extract population densities
XP2 = X[:,1]
XC1 = X[:,2]
XC2 = X[:,3]

shrub_ratio_1 = round(np.mean(XP2)/np.mean(XP1 + XP2),2)
browser_ratio_1 = round(np.mean(XC1)/np.mean(XC1 + XC2),2)

print("Simulation 1: ")
print("Shrub ratio: ", shrub_ratio_1)
print("Browser ratio: ", browser_ratio_1)

#--------------------------------------------------------------
# second time series
y0 = [0.2, 1.0, 0.1, 0.5]        # initial population densities
Y= integ.odeint(ss.savannas,y0,t, args = (fb, fd))   # integrate the system
YP1 = Y[:,0]                     # extract population densities
YP2 = Y[:,1]
YC1 = Y[:,2]
YC2 = Y[:,3]

shrub_ratio_2 = round(np.mean(YP2)/np.mean(YP1 + YP2),2)
browser_ratio_2 = round(np.mean(YC1)/np.mean(YC1 + YC2),2)

print("Simulation 2: ")
print("Shrub ratio: ", shrub_ratio_2)
print("Browser ratio: ", browser_ratio_2)

#---------------------------------------------------------------
# plot figure
plt.figure(figsize=(10,7))
tick_size = 15
label_size = 20

plt.style.use("default")
# plot first timeseries:
plt.subplot2grid((2,1), (0,0))

plt.plot(t, XP1, 'g-', label = 'Grasses ($P_H$)')
plt.plot(t, XP2, 'y-', label = 'Shrubs ($P_G$)')
plt.plot(t, XC1, 'r-', label = 'Browsers ($C_H$)')
plt.plot(t, XC2, 'm-', label = 'Grazers ($C_G$)')

plt.text(220,2.8,'ratio of shrubs within total plant population: {}'.format(shrub_ratio_1),fontsize = 17)
plt.text(220,2.35,'ratio of browsers within total animal population: {}'.format(browser_ratio_1), fontsize = 17)

plt.ylim(0.0,3.3)
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)  #hide legend 
plt.ylabel("Population density", fontsize = label_size)

# plot second time series:
plt.subplot2grid((2,1), (1,0))

plt.plot(t, YP1, 'g-', label = 'Grasses (P1)')
plt.plot(t, YP2, 'y-', label = 'Shrubs (P2)')
plt.plot(t, YC1, 'r-', label = 'Browsers (C1)')
plt.plot(t, YC2, 'm-', label = 'Grazers (C2)')

plt.text(220,2.8,'ratio of shrubs within total plant population: {}'.format(shrub_ratio_2), fontsize = 17)
plt.text(220,2.35,'ratio of browsers within total animal population: {}'.format(browser_ratio_2), fontsize = 17)

plt.ylim(0.0,3.3)
plt.xlabel("Time t", fontsize = label_size)
plt.ylabel("Population density", fontsize = label_size)

#save file to output folder
plt.tight_layout()
plt.savefig("output/Fig1b_time_series.pdf", dpi = 150)