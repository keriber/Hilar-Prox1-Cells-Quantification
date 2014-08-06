 # -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:52:00 2013

@author: kbermudez-hernandez
"""

import os
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import re
#Code to make list of files and vdevide them in slide1  and slide2
path = "G:\Keria\Quntification_CreBax\GCL\Area"
os.chdir(path)#change directory
from pandas import Series, DataFrame


FileNames=[]
Values = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        FileNames.append(os.path.basename(file)[:-4])
        Value = pd.read_table(file,sep='\t')
        Values.append(Value)

Data = dict(zip(FileNames,Values)) 
globals().update(Data)


                     
for file in FileNames:
    Data[file] = Data[file].rename(columns= {'Label':'SectionsID', 'Area':'GCL Area'})
    #Data[file]['Hilar Area']= Data[file]['Hilar Area'] * 0.136342782003905 
    Data[file].SectionsID = Data[file].SectionsID.str[:-4]
    X =  Data[file].SectionsID.str[0:2]
    Data[file].index = X.astype(int)
    Data[file].index.name ='Sections'

for file in FileNames:
    Data[file].to_csv(file + '_Area'+'.csv')

     