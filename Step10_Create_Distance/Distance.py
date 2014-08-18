# -*- coding: utf-8 -*-
"""
Created on Thu May 08 16:35:51 2014

@author: KBermudez-Hernandez
"""

import os
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats

##Cell Count---------------------------------------------------------------------------------------
# This is the path were the csv files with the count are
path = "C:\Users\KBermudez-Hernandez\Documents\Dropbox\Figures\Photoshop_ImageJ_Python_Scripts\Step10_Create_Distance"
os.chdir(path)#change directory
#If the ROI is the SGZ and the thext file if the coordinates of the ROI
ROI = pd.read_table('XY_01_CreBaxT5_3_pos_tamo_s2s1Deafult.txt')
EGC= pd.read_table('Ecotpics_T5_3_s1.txt')# the EGC will have the coordinates f the EGC
nodulo = np.array([1193.854,271.876])
#this fucntion returns the point in the array that has the closes point
def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    #node = np.asarray(node)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

EGC['Distance']=np.nan
  
#This will add the distance of eahc EGC from the edge of the SGZ
for z in range(0,len(EGC)):
    x = EGC.ix[z,'X']
    y = EGC.ix[z,'Y']
    nodulo = np.array([x,y])
    location = closest_node(nodulo,ROI)
    distance=np.linalg.norm(nodulo-ROI.ix[location])
    EGC.ix[z,'Distance']=distance
    print(distance)
    


location = closest_node(nodulo,ROI)