# -*- coding: utf-8 -*-
"""
Created on Mon Dec 02 11:24:07 2013

@author: kbermudez-hernandez
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:38:36 2013

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
path = "F:\Backup Seagate Hardrive\Quntification_CreBax\DefaultThreshold\SGZ_Files"
os.chdir(path)#change directory

cellstring = '_SGZ_cell_count' # string that indentifies the files with cell count
areastring = '_SGZ_Area'#string tha identifies fiels with Area

## Files that have cell count
listfiles =[]

for files in os.listdir(path):
    if files.endswith(".csv") and re.search(cellstring, files):
        listfiles.append(files)
       

##Files that Have SGZ Area
SGZ_listfiles=[]
for files in os.listdir(path):
     if files.endswith(".csv") and  re.search(areastring, files):
        SGZ_listfiles.append(files)
    

#merging both Files
All = []    
for i in range(0, len(listfiles)):
    if listfiles[i][:6] == SGZ_listfiles[i][:6]: ## Check this line
        cells = pd.read_csv(listfiles[i], index_col = 'Sections')
        sgz = pd.read_csv(SGZ_listfiles[i], index_col = 'Sections')
        if len(cells.index) == len(sgz.index):
            all = pd.concat([cells, sgz], axis= 1)
            name = re.sub(cellstring,' ',listfiles[i])
            all.columns.name = name[:-4]    
            All.append(all)
        else:
            print 'Error:The sections numbers are not the same for' + listfiles[i]
            continue


TotalCells = DataFrame(np.empty((14), dtype = np.float), index = range(1,15), columns = ['Nothing'])
SGZArea = DataFrame(np.empty((14), dtype = np.float), index = range(1,15), columns = ['Nothing'])

for index in All:
    TotalCells[index.columns.name]= index['Total Cells']
    SGZArea[index.columns.name]= index['SGZ Area']
 
del TotalCells['Nothing']
del SGZArea['Nothing']

TotalCells_Area = TotalCells/SGZArea


Negative_Corn = []
Negative_Tam = []
Positive_Corn = []
Positive_Tam = []

for i in TotalCells.columns:
    if re.search('neg', i) and re.search('corn', i):
        Negative_Corn.append(i)
    elif re.search('neg', i) and re.search('tamo', i):
        Negative_Tam.append(i)
    elif re.search('pos', i) and re.search('corn', i):
        Positive_Corn.append(i)
    else:
        Positive_Tam.append(i)
        
Groups = [Negative_Corn, Negative_Tam, Positive_Corn ,Positive_Tam ]
SGroup = ['Negative_Corn','Negative_Tam', 'Positive_Corn' ,'Positive_Tam' ]
Dictionary = dict(zip(SGroup,Groups))
Sorted_Groups=[]
for i in Groups:
    for x in i:
        Sorted_Groups.append(x)
        
    


#TotalCells
TotalCells=TotalCells.reindex(columns=Sorted_Groups)
SGZArea=SGZArea.reindex(columns=Sorted_Groups)
TotalCells_Area=TotalCells_Area.reindex(columns=Sorted_Groups)

for i, group  in enumerate(Groups):
    TotalCells[SGroup[i]+'_Mean'] = TotalCells[group].mean(axis =1)
    TotalCells[SGroup[i]+'_Values']= TotalCells[group].count(axis=1)
    TotalCells[SGroup[i]+'_Stdev'] = TotalCells[group].std(axis=1)
    TotalCells[SGroup[i]+'_Serror'] = TotalCells[SGroup[i]+'_Stdev']/np.sqrt(TotalCells[SGroup[i]+'_Values'])

#SGZArea
SGZArea=SGZArea.reindex(columns=Sorted_Groups)   
for i, group  in enumerate(Groups):
    SGZArea[SGroup[i]+'_Mean'] = SGZArea[group].mean(axis =1)
    SGZArea[SGroup[i]+'_Values']= SGZArea[group].count(axis=1)
    SGZArea[SGroup[i]+'_Stdev'] = SGZArea[group].std(axis=1)
    SGZArea[SGroup[i]+'_Serror'] = SGZArea[SGroup[i]+'_Stdev']/np.sqrt(SGZArea[SGroup[i]+'_Values'])

#Total Cells Devided by Area
TotalCells_Area=TotalCells_Area.reindex(columns=Sorted_Groups)
for i, group  in enumerate(Groups):
    TotalCells_Area[SGroup[i]+'_Mean'] = TotalCells_Area[group].mean(axis =1)
    TotalCells_Area[SGroup[i]+'_Values']= TotalCells_Area[group].count(axis=1)
    TotalCells_Area[SGroup[i]+'_Stdev'] = TotalCells_Area[group].std(axis=1)
    TotalCells_Area[SGroup[i]+'_Serror'] = TotalCells_Area[SGroup[i]+'_Stdev']/np.sqrt(TotalCells_Area[SGroup[i]+'_Values'])
## Saving Table

#TotalCells.to_csv('G:\Keria\Quntification_CreBax\DefaultThreshold\SGZ_Files\Summary\Total_Cells_CreBax_SGZ.csv')
#SGZArea.to_csv('G:\Keria\Quntification_CreBax\DefaultThreshold\SGZ_Files\Summary\SGZArea_CreBax_SGZ.csv')



#
def plotFigures(parameter,str1, str2,str3 = None,str4= None):
    ## Modify this part
    global TotalCells
    global SGZArea
    global TotalCells_Area
    global Dictionary
    
    
    dictionary = Dictionary
    plt.figure()   
    #plt.plot(parameter.index, parameter[dictionary[str1]], linestyle ='--', color = 'r' )
    plt.errorbar(parameter.index,parameter[str1 + '_Mean'] ,yerr=parameter[str1 + '_Serror'], color = 'r', marker ='o',label = 'Mean_'+ str1 )
    
    #plt.plot(parameter.index,parameter[dictionary[str2]], linestyle ='--', color = 'g' )
    plt.errorbar(parameter.index,parameter[str2 + '_Mean'] ,yerr=parameter[str2 + '_Serror'], color = 'g', marker ='o',label = 'Mean_'+ str2 )
    
    if str3 == None:
        print 'No group3'
    else:
        #plt.plot(parameter.index,parameter[dictionary[str3]], linestyle ='--', color = 'm' )
        plt.errorbar(parameter.index,parameter[str3 + '_Mean'] ,yerr=parameter[str3 + '_Serror'], color = 'm', marker ='o',label = 'Mean_'+ str3 )
    
    if str4 == None:
        print 'No Group4'        
    else:
        #plt.plot(parameter.index,parameter[dictionary[str4]], linestyle ='--', color = 'b' )
        plt.errorbar(parameter.index,parameter[str4 + '_Mean'] ,yerr=parameter[str4 + '_Serror'], color = 'b', marker ='o',label = 'Mean_'+ str4 )
    
    
    if np.array_equal(TotalCells.ix[:,1],parameter.ix[:,1]): 
        print 'yes'
        Title = 'Total Cells in SGZ'
        ylabel =' Prox1 cells'
    elif np.array_equal(SGZArea.ix[:,1],parameter.ix[:,1]): 
        Title = 'SGZ Area'
        ylabel =' SGZ Area'
    else:    
        Title = 'Prox1 cells Devided by area of SGZ'
        ylabel= 'Prox1 cells Devided by area of SGZ'
    
      
    plt.title(Title) # will set the title of the graph
    plt.xlabel('Section Number' ) #will set the x axis title
    plt.ylabel(ylabel)    
    plt.legend(loc ='best')   
    plt.xlim(xmax=15)
    
plotFigures(TotalCells,'Negative_Corn','Negative_Tam','Positive_Corn','Positive_Tam')
plotFigures(SGZArea,'Negative_Corn','Negative_Tam','Positive_Corn','Positive_Tam')
plotFigures(TotalCells_Area,'Negative_Corn','Negative_Tam','Positive_Corn','Positive_Tam')


   
##Saving Figures---------------------------------------------------------------------------------
#
#fig.savefig('Figures\\Prox1_SGZ_Cells.png', dpi = 400, bbox_inches = 'tight') 
#fig2.savefig('Figures\\SGZ_Area.png', dpi = 400, bbox_inches = 'tight') 
#fig3.savefig('Figures\\Prox1 Cells_SGZ Area.png', dpi = 400, bbox_inches = 'tight')