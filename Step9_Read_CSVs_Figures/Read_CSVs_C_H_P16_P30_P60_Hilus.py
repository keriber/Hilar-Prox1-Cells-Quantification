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
path = "F:\Backup Seagate Hardrive\Quantification_C57_SW\Quantification_Default_GCL_H\Hilus_CSV_copy"
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
        sgz = pd.read_csv(Hilus_listfiles[i], index_col = 'Sections')
        if len(cells.index) == len(sgz.index):
            all = pd.concat([cells, sgz], axis= 1)
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
    HilusArea[index.columns.name]= index['Hilus Area']
 
del TotalCells['Nothing']
del HilusArea['Nothing']

TotalCells_Area = TotalCells/HilusArea


C57_p30 = []
C57_p16 =[]
C57 = []
SW_p30 = []
SW= []
C57_p16_C_H =[]
C57_p30_C_H =[]
C57_p60_C_H =[]

for i in TotalCells.columns:
    if re.search('C57', i) and re.search('p16_C_H',i):
        C57_p16_C_H.append(i)
    elif re.search('C57', i) and re.search('p16',i):
        C57_p16.append(i)
    elif re.search('C57', i) and re.search('p30_C_H',i):
        C57_p30_C_H.append(i)
    elif re.search('C57', i) and re.search('p30', i):
        C57_p30.append(i)
    elif re.search('C57', i) and re.search('p60_C_H', i):
        C57_p60_C_H.append(i)    
    elif re.search('C57', i) and re.search('_', i):
        C57.append(i)
    elif re.search('SW', i) and re.search('p30', i):
        SW_p30.append(i)
    else:
       SW.append(i)
        
Groups = [C57_p16_C_H, C57_p30_C_H,C57_p60_C_H, C57_p16, C57_p30, C57, SW_p30 ,SW ]
SGroup = ['C57_p16_C_H','C57_p30_C_H','C57_p16','C57_p60_C_H','C57_p30','C57', 'SW_p30' ,'SW' ]
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

TotalCells.to_csv('C:\Users\KBermudez-Hernandez\Documents\Dropbox\Figures\Figure2  p16 p30 p60 Septotemporal\Hilus\Total_Cells_C57_SW_Hilus.csv')
HilusArea.to_csv('C:\Users\KBermudez-Hernandez\Documents\Dropbox\Figures\Figure2  p16 p30 p60 Septotemporal\Hilus\HilusArea_C57_SW_Hilus.csv')
TotalCells_Area.to_csv('C:\Users\KBermudez-Hernandez\Documents\Dropbox\Figures\Figure2  p16 p30 p60 Septotemporal\Hilus\Total_Cells_Area_C57_SW_Hilus.csv')

 TotalCells[Dictionary['C57_p30']]
 TotalCells[Dictionary['C57']]
#Calculating Density  Bar  Graph for C57 and C57_p30
 
TotalCellsSum = TotalCells.sum()
HilusAreaSum = HilusArea.sum()     
Density = TotalCellsSum/HilusAreaSum
DensityTable = Series([Density[Dictionary['C57_p16']].mean(),Density[Dictionary['C57_p30']].mean(),Density[Dictionary['C57']].mean()], index =['C57 P16','C57 P30','C57 P60'])
C57_p16_Error =Density[Dictionary['C57_p16']].std()/sqrt(Density[Dictionary['C57_p16']].count())
C57_p30_Error = Density[Dictionary['C57_p30']].std()/sqrt(Density[Dictionary['C57_p30']].count())
C57_Error = Density[Dictionary['C57']].std()/sqrt(Density[Dictionary['C57']].count())

#Density.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure1 p16 p30 p60 density\Prox_density_bar_graph\P16 P30 P60 Prox1 Density.csv')
TotalCellsSum.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure1 p16 p30 p60 density\Prox_density_bar_graph\P16 P30 P60 Prox1 Total_Cells.csv')
HilusAreaSum.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure1 p16 p30 p60 density\Prox_density_bar_graph\P16 P30 P60 Prox1 Hilus Are.csv')

#Plotting Density Bar Graph
plt.figure()
DensityTable.plot(kind='bar',
                  yerr=[C57_p16_Error,C57_p30_Error,C57_Error],
                  color='g',
                  capsize=6,
                  linewidth=3
                  )
plt.ylabel('Density of Prox1 in Hilus',size=20)
plt.xticks(size = 20, rotation=0)
plt.yticks(size = 14, rotation=0)
# Density Bar Graph  SW and C57

DensityTableSW_C57 = Series([Density[Dictionary['C57_p30']].mean(),Density[Dictionary['SW_p30']].mean(),Density[Dictionary['C57']].mean(),Density[Dictionary['SW']].mean()], index =['C57 P30','SW P30','C57 P60','SW'])
SW_p30_Error = Density[Dictionary['SW_p30']].std()/sqrt(Density[Dictionary['SW_p30']].count())
SW_Error = Density[Dictionary['SW']].std()/sqrt(Density[Dictionary['SW']].count())

plt.figure()   
DensityTableSW_C57.plot(kind='bar',yerr=[C57_p30_Error,SW_p30_Error,C57_Error,SW_Error],color='y')
plt.ylabel('Density of Prox1 in Hilus')
plt.xticks(rotation=0)
DensityTableSW_C57.to_csv('C:\Users\keriambermudez\Dropbox\Figures\Figure4 Strains\New folder\C57_SW_Density.csv')

## PLotting Hilus area Bar Graph

Table_Area_SW_C57 = Series([HilusAreaSum[Dictionary['C57_p16']].mean(),HilusAreaSum[Dictionary['C57_p30']].mean(),HilusAreaSum[Dictionary['SW_p30']].mean(),HilusAreaSum[Dictionary['C57']].mean(),HilusAreaSum[Dictionary['SW']].mean()], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])
Table_Area_SW_C57_STD = Series([HilusAreaSum[Dictionary['C57_p16']].std(),HilusAreaSum[Dictionary['C57_p30']].std(),HilusAreaSum[Dictionary['SW_p30']].std(),HilusAreaSum[Dictionary['C57']].std(),HilusAreaSum[Dictionary['SW']].std()], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])
Table_Area_SW_C57_Error = Table_Area_SW_C57_STD/SQRT
plt.figure()   
Table_Area_SW_C57.plot(kind='bar',yerr=TableSW_C57_Error,color='y')
plt.ylabel('Hilus Area')
plt.xticks(rotation=0)

## PLotting Total Cells Bar Graph

Table_Cells_SW_C57 = Series([TotalCellsSum[Dictionary['C57_p16']].mean(),TotalCellsSum[Dictionary['C57_p30']].mean(),TotalCellsSum[Dictionary['SW_p30']].mean(),TotalCellsSum[Dictionary['C57']].mean(),TotalCellsSum[Dictionary['SW']].mean()], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])
Table_Cells_SW_C57_STD = Series([TotalCellsSum[Dictionary['C57_p16']].std(),TotalCellsSum[Dictionary['C57_p30']].std(),TotalCellsSum[Dictionary['SW_p30']].std(),TotalCellsSum[Dictionary['C57']].std(),TotalCellsSum[Dictionary['SW']].std()], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])
SQRT= Series([sqrt(TotalCellsSum[Dictionary['C57_p16']].count()),sqrt(TotalCellsSum[Dictionary['C57_p30']].count()),sqrt(TotalCellsSum[Dictionary['SW_p30']].count()),sqrt(TotalCellsSum[Dictionary['C57']].count()),sqrt(TotalCellsSum[Dictionary['SW']].count())], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])
Table_Cells_SW_C57_Error = Table_Cells_SW_C57_STD/SQRT
plt.figure()   
Table_Cells_SW_C57.plot(kind='bar',yerr=Table_Cells_SW_C57_Error,color='y')
plt.ylabel('Total Cells')
plt.xticks(rotation=0)



#Coronals and Horizontals Desnity

C57_p30_C_Density =  TotalCells.ix[1:5,Dictionary['C57_p30_C_H']].sum()/HilusArea.ix[1:5,Dictionary['C57_p30_C_H']].sum()
C57_p30_H_Density = TotalCells.ix[6:10,Dictionary['C57_p30_C_H']].sum()/HilusArea.ix[6:10,Dictionary['C57_p30_C_H']].sum()
C57_p16_C_Density =  TotalCells.ix[1:5,Dictionary['C57_p16_C_H']].sum()/HilusArea.ix[1:5,Dictionary['C57_p16_C_H']].sum()
C57_p16_H_Density = TotalCells.ix[6:10,Dictionary['C57_p16_C_H']].sum()/HilusArea.ix[6:10,Dictionary['C57_p16_C_H']].sum()

DensityTable_C_H = Series([C57_p16_C_Density.mean(),C57_p16_H_Density.mean(),C57_p30_C_Density.mean(),C57_p30_H_Density.mean()],index =['C57 P16 Coron','C57 P16 Horiz','C57 P30 Coro', 'C57 P30 Horizo'])

C57_p16_C_Density_Error = C57_p16_C_Density.std()
C57_p16_H_Density_Error = C57_p16_C_Density.std()
C57_p30_C_Density_Error = C57_p30_C_Density.std()
C57_p30_H_Density_Error = C57_p30_C_Density.std()
plt.figure() 
DensityTable_C_H.plot(kind='bar', yerr=[C57_p16_C_Density_Error,C57_p16_H_Density_Error,C57_p30_C_Density_Error,C57_p30_H_Density_Error],color='g')

#DensityTable_C_H.plot(kind='bar',color='g')

plt.ylabel('Density of Prox1 in Hilus',size=20)
plt.xticks(rotation=0, size=14)
plt.yticks( size=14)
#Total Cells

C57_p30_C_Sum =  TotalCells.ix[1:5,Dictionary['C57_p30_C_H']].sum()
C57_p30_H_Sum = TotalCells.ix[6:10,Dictionary['C57_p30_C_H']].sum()
C57_p16_C_Sum =  TotalCells.ix[1:5,Dictionary['C57_p16_C_H']].sum()
C57_p16_H_Sum = TotalCells.ix[6:10,Dictionary['C57_p16_C_H']].sum()

Table_C_H = Series([C57_p16_C_Sum.mean(),C57_p16_H_Sum.mean(),C57_p30_C_Sum.mean(),C57_p30_H_Sum.mean()],index =['C57 P16 Coron','C57 P16 Horiz','C57 P30 Coro', 'C57 P30 Horizo'])

C57_p16_C_Sum_Error = C57_p16_C_Sum.std()
C57_p16_H_Sum_Error = C57_p16_C_Sum.std()
C57_p30_C_Sum_Error = C57_p30_C_Sum.std()
C57_p30_H_Sum_Error = C57_p30_C_Sum.std()


plt.figure() 
Table_C_H.plot(kind='bar', yerr=[C57_p16_C_Sum_Error,C57_p16_H_Sum_Error,C57_p30_C_Sum_Error,C57_p30_H_Sum_Error],color='g')
plt.ylabel('Total Cells')
plt.xticks(rotation=0)

#Hilar Area


C57_p30_C_Area =  HilusArea.ix[1:5,Dictionary['C57_p30_C_H']].sum()
C57_p30_H_Area = HilusArea.ix[6:10,Dictionary['C57_p30_C_H']].sum()
C57_p16_C_Area =  HilusArea.ix[1:5,Dictionary['C57_p16_C_H']].sum()
C57_p16_H_Area = HilusArea.ix[6:10,Dictionary['C57_p16_C_H']].sum()

Table_C_H_Area = Series([C57_p16_C_Area.mean(),C57_p16_H_Area.mean(),C57_p30_C_Area.mean(),C57_p30_H_Area.mean()],index =['C57 P16 Coron','C57 P16 Horiz','C57 P30 Coro', 'C57 P30 Horizo'])

C57_p16_C_Area_Error = C57_p16_C_Area.std()
C57_p16_H_Area_Error = C57_p16_C_Area.std()
C57_p30_C_Area_Error = C57_p30_C_Area.std()
C57_p30_H_Area_Error = C57_p30_C_Area.std()


plt.figure() 
Table_C_H_Area.plot(kind='bar', yerr=[C57_p16_C_Area_Error,C57_p16_H_Area_Error,C57_p30_C_Area_Error,C57_p30_H_Area_Error],color='g')
plt.ylabel('Total Cells')
plt.xticks(rotation=0)



def plotFigures(parameter,str1, str2,str3 = None,str4= None):
    ## Modify this part
    global TotalCells
    global HilusArea
    global TotalCells_Area
    global Dictionary
      
    dictionary = Dictionary
    plt.figure()   
    #plt.plot(parameter.index, parameter[dictionary[str1]], linestyle ='--', color = 'r' )
    plt.errorbar(parameter.index[0:12],parameter.ix[0:12,str1 + '_Mean'] ,yerr=parameter.ix[0:12,str1 + '_Serror'], color = 'r', marker ='o',label = 'Mean_'+ str1 )
    
    #plt.plot(parameter.index,parameter[dictionary[str2]], linestyle ='--', color = 'g' )
    plt.errorbar(parameter.index[0:12],parameter.ix[0:12,str2 + '_Mean'] ,yerr=parameter.ix[0:12,str2 + '_Serror'], color = 'g', marker ='o',label = 'Mean_'+ str2 )
    
    if str3 == None:
        print 'No group3'
    else:
        #plt.plot(parameter.index,parameter[dictionary[str3]], linestyle ='--', color = 'm' )
        plt.errorbar(parameter.index[0:12],parameter.ix[0:12,str3 + '_Mean'] ,yerr=parameter.ix[0:12,str3 + '_Serror'], color = 'm', marker ='o',label = 'Mean_'+ str3 )
    
    if str4 == None:
        print 'No Group4'        
    else:
        #plt.plot(parameter.index,parameter[dictionary[str4]], linestyle ='--', color = 'b' )
        plt.errorbar(parameter.index[0:12],parameter.ix[0:12,str4 + '_Mean'] ,yerr=parameter.ix[0:12,str4 + '_Serror'], color = 'b', marker ='o',label = 'Mean_'+ str4 )
    
    
    if np.array_equal(TotalCells.ix[1,1],parameter.ix[1,1]): 
        print 'yes'
        Title = 'Total Cells'
        ylabel =' Prox1 cells'
    elif np.array_equal(HilusArea.ix[1,1],parameter.ix[1,1]): 
        Title = 'Hilus Area'
        ylabel =' Hilus Area'
    else:    
        Title = 'Prox1 cells Devided by area'
        ylabel= 'Prox1 cells Devided by area'
      
    plt.title(Title,size=20) # will set the title of the graph
    plt.xlabel('Section Number',size=14 ) #will set the x axis title
    plt.ylabel(ylabel,size=14)    
    plt.legend(loc ='best')   
    plt.xlim(xmax=13)
    
plotFigures(TotalCells,'C57_p30','SW_p30','C57','SW')
plotFigures(HilusArea,'C57_p30','SW_p30','C57','SW')
plotFigures(TotalCells_Area,'C57_p30','SW_p30')
plotFigures(TotalCells_Area,'C57','SW')
plotFigures(TotalCells,'C57','SW')
plotFigures(TotalCells,'C57_p30','SW_p30')
plotFigures(TotalCells,'C57_p30','C57')  
plotFigures(TotalCells_Area,'C57_p30','C57') 
plotFigures(HilusArea,'C57_p30','C57')
plotFigures(TotalCells, 'C57_p16','C57_p30','C57')
plotFigures(TotalCells_Area, 'C57_p16','C57_p30','C57')
plotFigures(HilusArea, 'C57_p16','C57_p30','C57')
plotFigures(TotalCells,'C57_p16_C_H','C57_p30_C_H')
plotFigures(TotalCells_Area,'C57_p16_C_H','C57_p30_C_H')
# Comparison of 
fig = plt.figure()
ax1= fig.add_subplot(2,1,1)
plotFigures(TotalCells,'C57_p30','C57')  
#plt.legend(loc ='best')   
ax2= fig.add_subplot(2,1,2)
plotFigures(TotalCells_Area,'C57_p30','C57') 
#plt.legend(loc ='best')


#Comparison of Strain Total Cells amd Density
fig = plt.figure()
ax1= fig.add_subplot(2,2,1)
plotFigures(TotalCells,'C57_p30','SW_p30')
plt.ylim(ymax=60)  
plt.legend(loc ='best')   
ax2= fig.add_subplot(2,2,2)
plotFigures(TotalCells_Area,'C57_p30','SW_p30') 
plt.legend(loc ='best')
plt.ylim(ymax=0.0007)  
ax4= fig.add_subplot(2,2,3)
plotFigures(TotalCells,'C57','SW')  
plt.legend(loc ='best')
plt.ylim(ymax=60)     
ax4= fig.add_subplot(2,2,4)
plotFigures(TotalCells_Area,'C57','SW') 
plt.legend(loc ='best')
plt.ylim(ymax=0.0007)  

#Comparison of Strain Area

fig = plt.figure()
ax1= fig.add_subplot(1,2,1)
plotFigures(HilusArea,'C57_p30','SW_p30')  

plt.ylim(ymax=200000)  
plt.legend(loc ='best') 
ax2= fig.add_subplot(1,2,2)
plotFigures(HilusArea,'C57','SW') 

plt.ylim(ymax=200000)
plt.legend(loc ='best')
##Saving Figures---------------------------------------------------------------------------------
#
#fig.savefig('Figures\\Prox1_Hilus_Cells.png', dpi = 400, bbox_inches = 'tight') 
#fig2.savefig('Figures\\Hilus_Area.png', dpi = 400, bbox_inches = 'tight') 
#fig3.savefig('Figures\\Prox1 Cells_Hilus Area.png', dpi = 400, bbox_inches = 'tight')