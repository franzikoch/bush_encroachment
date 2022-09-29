"""
Create Figure S1: Plot of all feedback loop weights at the unstable fixed point

Input needed: csv table of loop weight ("unstable_points_Fk_values.csv") created by total_feedback.py

"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


#read in csv file
Fk_unstable = pd.read_csv('unstable_points_Fk_values.csv', index_col = 0)

#create plot

#set font sizes 
title_size = 22
label_size = 22
tick_size = 16
m_size = 10
#plot one graph for each state, showing all loops
#erstmal alle mehrere loops in einen graph
f = plt.figure(figsize = (10,10))

#2 link loops
plt.plot(Fk_unstable['fb'], Fk_unstable['a12a21'], 'v', label = "grasses-shrubs")
plt.plot(Fk_unstable['fb'], Fk_unstable['a13a31'], 'v', label = "grasses-browsers")
plt.plot(Fk_unstable['fb'], Fk_unstable['a14a41'], 'v', label = "grasses-grazers")
plt.plot(Fk_unstable['fb'], Fk_unstable['a23a32'], 'v', label = "shrubs-browsers")
plt.plot(Fk_unstable['fb'], Fk_unstable['a24a42'], 'v', label = "shrubs-grasses")

#3 link loops
plt.plot(Fk_unstable['fb'], Fk_unstable['a21a42a14'], '.', markersize = m_size, label = "grasses -> shrubs \n -> grazers -> grasses")
plt.plot(Fk_unstable['fb'], Fk_unstable['a41a24a12'], '.', markersize = m_size, label = "grasses -> grazers \n -> shrubs -> grasses")
plt.plot(Fk_unstable['fb'], Fk_unstable['a31a23a12'], '.', markersize = m_size, label = "grasses -> browsers \n -> shrubs -> grasses")
plt.plot(Fk_unstable['fb'], Fk_unstable['a21a32a13'], '.', markersize = m_size, label = "grasses -> shrubs \n -> browsers -> grasses")

#4 link loops
plt.plot(Fk_unstable['fb'], Fk_unstable['a41a24a32a13'], '*', markersize = m_size ,label = "grasses -> grazers -> shrubs \n -> browsers -> grasses")
plt.plot(Fk_unstable['fb'], Fk_unstable['a31a23a42a14'], '*', markersize = m_size, label = "grasses -> browsers -> shrubs \n -> grazers -> grasses")


#mark bifurcation point + extinction of browsers
plt.axhline(y = 0, color = "black")

plt.xlabel("$f_b, f_d = 0$", fontsize = label_size)
plt.ylabel("loop weight [1/t]", fontsize = label_size)
plt.legend(bbox_to_anchor= (1.1,1), fontsize = label_size)


plt.yticks(fontsize = tick_size)
plt.xticks(fontsize = tick_size)

#save fig
plt.savefig("loop_weights_unstable_point.png", bbox_inches='tight', dpi = 300)
