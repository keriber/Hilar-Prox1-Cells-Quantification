# -*- coding: utf-8 -*-
"""
Created on Wed Nov 06 09:26:31 2013

@author: kbermudez-hernandez
"""
import os
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
#Code to make list of files and vdevide them in slide1  and slide2


path = "G:\Keria\Quntification_CreBax\DefaultThreshold\CreBaxT103_pos_tamo\SGZ"
name = 'CreBaxT103_pos_tamo'
os.chdir(path)#change directory

listfiles =[]
for files in os.listdir(path):
    if files.endswith(".txt"):
        listfiles.append(files)
        
##Sections
#            
SectionsID = []
Sections = []
for index in listfiles:
    SectionsID.append(index[:-8])
    Sections.append(index[0:2])

#Data       
data = []
for index in listfiles:
    temp=pd.read_table(index)
    temp3=np.array(temp['Area'])
    data.append(temp3)
#Cells
cells_temp = []
for index in data:
    newindex = np.where(index < 50.26, index, 0 )
    cells_temp.append(newindex)
cells=[]
for index in cells_temp:
    newindex = np.where(index > 15.0, index, 0 )
    cells.append(newindex)
#Cell Count and CellsArea
cellCount =[]
cellsArea = []
for index in cells:
    cellCount.append(np.count_nonzero(index))
    
for index in cells:
    cellsArea.append(np.sum(index))

# Clusters
    
clusters =[]  
for index in data:
    newindex = np.where(index >= 50.26, index,0)     
    clusters.append(newindex)   
#Cluster Count
clusterCount =[]
clusterArea = []
for index in clusters:
    clusterCount.append(np.count_nonzero(index))
    
for index in clusters:
    clusterArea.append(np.sum(index))

clusterCount = np.array(clusterArea)/37.39

totalCells = np.array(cellCount)+clusterCount
#Making Dataframe Table
Dictionary = {'Cell Count':dict(zip(Sections,cellCount)),
              'Cells Total Area':dict(zip(Sections,cellsArea)),
              'Cluster Area': dict(zip(Sections,clusterArea)),
              'Cluster Count': dict(zip(Sections,clusterCount)),'Total Cells': dict(zip(Sections,totalCells)),
              'SectionsID': dict(zip(Sections, SectionsID))} 
   
Table = DataFrame(Dictionary, columns=['SectionsID','Cell Count','Cells Total Area', 'Cluster Count','Cluster Area', 'Total Cells'])
Table.index.name = 'Sections'


Table.to_csv(name + '_SGZ_cell_count'+'.csv')

#name = path[62:].replace('\\', '_')




















#cells = np.array(cells)
#clusters = np.array(clusters)

###Count 
#Cells = []
#Clusters = []
#for i in range(0,len(data)):
#    for index in data:
#        for x in range(0,len(index)):
#            if index[x] >= 12.56 and index[x] <=5no0.26:
#               Cells[i] = np.array(index[x])
#            else:
#                Clusters[i].insert(index[x])
#    
    #Count.append(len(index))
##Area
#Area = []
#for index in data:
#    Area.append(sum(index))
#    
#    
##Making Dataframe Table
#Dictionary = {'Count':dict(zip(Sections,Count)), 'Area': dict(zip(Sections,Area)),'SectionsID': dict(zip(Sections, SectionsID))} 
#   
#Table = DataFrame(Dictionary, columns=['Sections','Count','Area'])
#
#name = path[62:].replace('\\', '_')
#Table.to_csv(name +'.csv')
#

  