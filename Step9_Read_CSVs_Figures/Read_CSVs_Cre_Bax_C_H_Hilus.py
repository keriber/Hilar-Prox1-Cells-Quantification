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
path = "F:\Backup Seagate Hardrive\CreBax\CSV_Files"
os.chdir(path)#change directory

cellstring = '_Hilus_cell_count' # string that indentifies the files with cell count
areastring = '_Hilus_Area'#string tha identifies fiels with Area

## Files that have cell count
listfiles =[]

for files in os.listdir(path):
    if files.endswith(".csv") and re.search(cellstring, files):
        listfiles.append(files)
       

##Files that Have Hilus Area
Hilus_listfiles=[]
for files in os.listdir(path):
     if files.endswith(".csv") and  re.search(areastring, files):
        Hilus_listfiles.append(files)
    

#merging both Files
All = []    
for i in range(0, len(listfiles)):
    if listfiles[i][:6] == Hilus_listfiles[i][:6]: ## Check this line
        cells = pd.read_csv(listfiles[i], index_col = 'Sections')
        hilus = pd.read_csv(Hilus_listfiles[i], index_col = 'Sections')
        if len(cells.index) == len(hilus.index):
            all = pd.concat([cells, hilus], axis= 1)
            name = re.sub(cellstring,' ',listfiles[i])
            all.columns.name = name[:-4]    
            All.append(all)
        else:
            print 'Error:The sections numbers are not the same for' + listfiles[i]
            continue


TotalCells = DataFrame(np.empty((14), dtype = np.float), index = range(1,15), columns = ['Nothing'])
HilusArea = DataFrame(np.empty((14), dtype = np.float), index = range(1,15), columns = ['Nothing'])

for index in All:
    TotalCells[index.columns.name]= index['Total Cells']
    HilusArea[index.columns.name]= index['Hilar Area']
 
del TotalCells['Nothing']
del HilusArea['Nothing']

TotalCells_Area = TotalCells/HilusArea


P30_Positive_Tam = []
P30_Negative_Tam = []
P60_Positive_Tam = []
P60_Negative_Tam = []

for i in TotalCells.columns:
    if re.search('P30', i) and re.search('neg', i):
        P30_Negative_Tam.append(i)
    elif re.search('P30', i) and re.search('pos', i):
        P30_Positive_Tam.append(i)
    elif re.search('P60', i) and re.search('neg', i):
        P60_Negative_Tam.append(i)
    else:
        P60_Positive_Tam.append(i)
        
Groups = [P30_Positive_Tam, P30_Negative_Tam, P60_Positive_Tam ,P60_Negative_Tam ]
SGroup = ['P30_Positive_Tam','P30_Negative_Tam', 'P60_Positive_Tam' ,'P60_Negative_Tam' ]

Dictionary = dict(zip(SGroup,Groups))
Sorted_Groups=[]
for i in Groups:
    for x in i:
        Sorted_Groups.append(x)
        
    


#TotalCells
TotalCells=TotalCells.reindex(columns=Sorted_Groups)
HilusArea=HilusArea.reindex(columns=Sorted_Groups)
TotalCells_Area=TotalCells_Area.reindex(columns=Sorted_Groups)

for i, group  in enumerate(Groups):
    TotalCells[SGroup[i]+'_Mean'] = TotalCells[group].mean(axis =1)
    TotalCells[SGroup[i]+'_Values']= TotalCells[group].count(axis=1)
    TotalCells[SGroup[i]+'_Stdev'] = TotalCells[group].std(axis=1)
    TotalCells[SGroup[i]+'_Serror'] = TotalCells[SGroup[i]+'_Stdev']/np.sqrt(TotalCells[SGroup[i]+'_Values'])

#HilusArea
HilusArea=HilusArea.reindex(columns=Sorted_Groups)   
for i, group  in enumerate(Groups):
    HilusArea[SGroup[i]+'_Mean'] = HilusArea[group].mean(axis =1)
    HilusArea[SGroup[i]+'_Values']= HilusArea[group].count(axis=1)
    HilusArea[SGroup[i]+'_Stdev'] = HilusArea[group].std(axis=1)
    HilusArea[SGroup[i]+'_Serror'] = HilusArea[SGroup[i]+'_Stdev']/np.sqrt(HilusArea[SGroup[i]+'_Values'])

#Total Cells Devided by Area
TotalCells_Area=TotalCells_Area.reindex(columns=Sorted_Groups)
for i, group  in enumerate(Groups):
    TotalCells_Area[SGroup[i]+'_Mean'] = TotalCells_Area[group].mean(axis =1)
    TotalCells_Area[SGroup[i]+'_Values']= TotalCells_Area[group].count(axis=1)
    TotalCells_Area[SGroup[i]+'_Stdev'] = TotalCells_Area[group].std(axis=1)
    TotalCells_Area[SGroup[i]+'_Serror'] = TotalCells_Area[SGroup[i]+'_Stdev']/np.sqrt(TotalCells_Area[SGroup[i]+'_Values'])
## Saving Table

TotalCells.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure3 Cre Bax\Coronals_Horizontals\Total_Cells_CreBax_C_H_Hilus.csv')
HilusArea.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure3 Cre Bax\Coronals_Horizontals\HilusArea_CreBax_C_H_Hilus.csv')
TotalCells_Area.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure3 Cre Bax\Coronals_Horizontals\Total_Cells_Area_C_H_CreBax_Hilus.csv')



#Calculating Density of All
 
TotalCellsSum = TotalCells.sum()
HilusAreaSum = HilusArea.sum()     
Density = TotalCellsSum/HilusAreaSum

DensityTable = Series([Density[P30_Positive_Tam].mean(),Density[P30_Negative_Tam].mean(),Density[P60_Positive_Tam].mean(),Density[P60_Negative_Tam].mean()], index =['P30_Positive_Tam','P30_Negative_Tam', 'P60_Positive_Tam' ,'P60_Negative_Tam'])
P30_Positive_Tam_Error =Density[P30_Positive_Tam].std()/sqrt(Density[P30_Positive_Tam].count())
P30_Negative_Tam_Error = Density[P30_Negative_Tam].std()/sqrt(Density[P30_Negative_Tam].count())
P60_Positive_Tam_Error = Density[P60_Positive_Tam].std()/sqrt(Density[P60_Positive_Tam].count())
P60_Negative_Tam_Error = Density[P60_Negative_Tam].std()/sqrt(Density[P60_Negative_Tam].count())



#Density.to_csv('C:\Users\KBermudez-Hernandez\Documents\Dropbox\Figures\Figure1 p16 p30 p60 density\Prox_density_bar_graph\P16 P30 P60 Prox1 Density.csv')

#Plotting Density Graph
plt.figure()   
DensityTable['P60_Positive_Tam':'P60_Negative_Tam'].plot(kind='bar',yerr=[P60_Positive_Tam_Error,P60_Negative_Tam_Error],color='g')
plt.ylabel('Density of Prox1 in Hilus')
plt.xticks(rotation=0)


#Coronals Vs Horizontals
#P30
P60_Positive_C =  TotalCells.ix[1:4,Dictionary['P30_Positive_Tam']].sum()/HilusArea.ix[1:4,Dictionary['P30_Positive_Tam']].sum()
P30_Positive_H = TotalCells.ix[5:8,Dictionary['P30_Positive_Tam']].sum()/HilusArea.ix[5:8,Dictionary['P30_Positive_Tam']].sum()
P30_Negative_C =  TotalCells.ix[1:4,Dictionary['P30_Negative_Tam']].sum()/HilusArea.ix[1:4,Dictionary['P30_Negative_Tam']].sum()
P30_Negative_H = TotalCells.ix[5:8,Dictionary['P30_Negative_Tam']].sum()/HilusArea.ix[5:8,Dictionary['P30_Negative_Tam']].sum()

#P60
P60_Positive_C =  TotalCells.ix[1:4,Dictionary['P60_Positive_Tam']].sum()/HilusArea.ix[1:4,Dictionary['P60_Positive_Tam']].sum()
P60_Positive_H = TotalCells.ix[5:8,Dictionary['P60_Positive_Tam']].sum()/HilusArea.ix[5:8,Dictionary['P60_Positive_Tam']].sum()
P60_Negative_C =  TotalCells.ix[1:4,Dictionary['P60_Negative_Tam']].sum()/HilusArea.ix[1:4,Dictionary['P60_Negative_Tam']].sum()
P60_Negative_H = TotalCells.ix[5:8,Dictionary['P60_Negative_Tam']].sum()/HilusArea.ix[5:8,Dictionary['P60_Negative_Tam']].sum()

P60_C_H = pd.merge([P60_Positive_C, P60_Positive_H,P60_Negative_C,P60_Negative_H], axis= 1)
P60_C_H.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure3 Cre Bax\Coronals_Horizontals\C_H_Density_ForAnova.csv')
DensityTable_C_H_P60 = Series([P60_Positive_C.mean(),P60_Negative_C.mean(),P60_Positive_H.mean(),P60_Negative_H.mean()],index =['Positive Coron','Negative Coron','Positive Hori', 'Negative Hori'])
DensityTable_Error = Series([P60_Positive_C.std()/sqrt(P60_Positive_C.count()),P60_Negative_C.std()/sqrt(P60_Negative_C.count()),P60_Positive_H.std()/sqrt(P60_Positive_H.count()),P60_Negative_H.std()/sqrt(P60_Negative_H.count())],index =['Positive Coron','Negative Coron','Positive Hori', 'Negative Hori'])


plt.figure() 
DensityTable_C_H_P60.plot(kind='bar', yerr=DensityTable_Error,color='g')
plt.ylabel('Density of Prox1 in Hilus')
plt.xticks(rotation=0)







#
def plotFigures(parameter,str1, str2,str3 = None,str4= None):
    ## Modify this part
    global TotalCells
    global HilusArea
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
    if np.array_equal(TotalCells.ix[2,2],parameter.ix[2,2]): 
        print 'yes'
        Title = 'Total Cells'
        ylabel =' Prox1 cells'
    elif np.array_equal(HilusArea.ix[2,2],parameter.ix[2,2]): 
        Title = 'Hilus Area'
        ylabel =' Hilus Area'
    else:    
        Title = 'Prox1 cells Devided by area'
        ylabel= 'Prox1 cells Devided by area'
    plt.title(Title) # will set the title of the graph
    plt.xlabel('Section Number' ) #will set the x axis title
    plt.ylabel(ylabel)    
    plt.legend(loc ='best')   
    plt.xlim(xmax=15)
      
   
    
    
plotFigures(TotalCells,'P60_Positive_Tam' ,'P60_Negative_Tam' )
plotFigures(HilusArea,'P60_Positive_Tam' ,'P60_Negative_Tam')
plotFigures(TotalCells_Area,'P60_Positive_Tam' ,'P60_Negative_Tam')


   
##Saving Figures---------------------------------------------------------------------------------
#
#fig.savefig('Figures\\Prox1_Hilus_Cells.png', dpi = 400, bbox_inches = 'tight') 
#fig2.savefig('Figures\\Hilus_Area.png', dpi = 400, bbox_inches = 'tight') 
#fig3.savefig('Figures\\Prox1 Cells_Hilus Area.png', dpi = 400, bbox_inches = 'tight')