#import modules
from sympy import *
import numpy as np
import random as rd
import pandas as pd

#-----------------------------------------------------------------------
#Define functions
#----------------------------------------------------------------------
def get_partial_derivs(equation_list, state_variables):
    
    """
    Calculates all partial derivatives of the system and returns them as a nested list
    """
    
    diffs = []

    for eq in equation_list:
        #loop through equations -> one row in the Jacobian
        row = []
        for var in state_variables:
            #ableiten nach jeder variablen
            x = diff(eq, var)
            row.append(x)
       
        #add row, which contains derivatives of one equation to all variables to full list
        diffs.append(row)

    return diffs
#------------------------------------------------------------------------
def get_jacobian(diffs, eq):
    
    """
    substitutes the equilibrium population densities into each partial derivative
    return Jacobian matrix as an array
    
    inputs: 
    -diffs -> nested list of partial derivatives
    -eq -> dictionary of the equilibrium densities of each state variable
    """
    
    Jacobian = [] #initialise list to collect Jacobian elements
    
    for row in diffs:
        Jac_row = []
        
        #loop through the elements of row
        for row_element in row:
            aij = float(row_element.subs(eq).evalf())
            Jac_row.append(aij)
        
        Jacobian.append(Jac_row)
  
    return np.array(Jacobian)
#-----------------------------------------------------------------------
def total_feedback(A):
    
    "calculates total feedback at levels 1,2,3,4 for a given matrix A"
    
    charpoly = np.poly(A)
    
    F1 = -charpoly[1]
    F2 = -charpoly[2]
    F3 = -charpoly[3]
    F4 = -charpoly[4]
    
    return F1, F2, F3, F4

#----------------------------------------------------------------------
#Define equations and parameters
#---------------------------------------------------------------------
#initialise all variables as symbols:
PH, PS, CB, CG = symbols('PH PS CB CG')
# initialise all plant parameters as symbols:
rH, rS,  KH, c, KS = symbols('rH rS KH c KS')
# initialise all animal parameters as symbols:
e, a, h, mb, md = symbols('e a h mb md')
#initialise feeding preferences
pHB, pHG, pSB, pSG = symbols('pHB pHG pSB pSG')
#farmer investment
fb = symbols('fb')

#all parameters, except for fb, are fixed 
our_parameter_set = {rH: 1, rS: 0.5, KH:2, KS:3, c:0.3, mb:0.15, md:0.05, e:0.45, a:1, h:3, pHB:0.3, pHG:0.7, pSB:0.7, pSG:0.3}

#define the four equations: 
fPH = rH*PH*(1-(PH + c*PS)/KH)- (a*PH*pHB/(1+a*h*PH*pHB))*CB- (a*PH*pHG/(1+a*h*PH*pHG))*CG
fPS = rS*PS*(1-(PS + c*PH)/KS)- (a*PS*pSB/(1+a*h*PS*pSB))*CB- (a*PS*pSG/(1+a*h*PS*pSG))*CG
fCB = e*(a*PH*pHB/(1+a*h*PH*pHB))*CB + e*(a*PS*pSB/(1+a*h*PS*pSB))*CB- mb*CB- md*CB**2            
fCG = e*(a*PH*pHG/(1+a*h*PH*pHG))*CG + e*(a*PS*pSG/(1+a*h*PS*pSG))*CG- mb*(1-fb)*CG- md*CG**2   

#substitute all parameters into the equations (except for fb)
fPH = fPH.subs(our_parameter_set)
fPS = fPS.subs(our_parameter_set)
fCB = fCB.subs(our_parameter_set)
fCG = fCG.subs(our_parameter_set)


#collect all equations and parameters in a list
equation_list = [fPH, fPS, fCB, fCG]
state_variables = [PH, PS, CB, CG]
#--------------------------------------------------------------------------
#get all partial derivatives:
diffs = get_partial_derivs(equation_list, state_variables)
#--------------------------------------------------------------------------
#read in equilibrium densities from csv files

encroached_points = pd.read_csv("encroached_states_densities.csv", index_col = 0)
grassy_points = pd.read_csv("grassy_states_densities.csv", index_col = 0)
unstable_points = pd.read_csv("unstable_fixed_points.csv")

f_values = np.array(unstable_points['fb'])


#-------------------------------------------------------------------------------

def get_all_Fks(points_df, f_values):
    
    "Calculates all total feedback values for a data frame of equilibrium densities"
    
    nrows = points_df.shape[0]
    
    all_Fks = []
    
    for f in f_values: #loop through the rows
        
        #select all rows in df with fb value
        row = points_df.loc[points_df['fb']==f]
        
        #create dictionary
        eq = {PH:float(row['PH']) , PS:float(row['PS']) , CB:float(row['CB']), CG:float(row['CG']), fb:f}
        
        Jacobian= get_jacobian(diffs, eq)
    
        F1, F2, F3, F4 = total_feedback(Jacobian)
    
        all_Fks.append([F1, F2, F3, F4])
        
    #turn results into a dataframe
    all_Fks = pd.DataFrame(all_Fks, columns = ["F1", "F2", "F3", "F4"])
    results = pd.concat([points_df, all_Fks], axis = 1)   
    
    return results
#---------------------------------------------------------------------------------

#calculate total feedback values
Fk_unstable = get_all_Fks(unstable_points, f_values)
Fk_encroached = get_all_Fks(encroached_points, f_values)
Fk_grassy = get_all_Fks(grassy_points, f_values)

#save value to csv file
Fk_unstable.to_csv("unstable_points_Fk_values.csv")
Fk_encroached.to_csv("encroached_points_Fk_values.csv")
Fk_grassy.to_csv("grassy_points_Fk_values.csv")