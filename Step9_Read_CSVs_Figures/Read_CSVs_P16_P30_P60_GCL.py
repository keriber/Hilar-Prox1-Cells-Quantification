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
path = "F:\Backup Seagate Hardrive\Quantification_C57_SW\Quantification_Default_GCL_H\GCL_CSVs"
os.chdir(path)#change directory


areastring = '_GCL_Area'#string tha identifies fiels with Area

      

##Files that Have Hilar Area
GCL_listfiles=[]
for files in os.listdir(path):
     if files.endswith(".csv") and  re.search(areastring, files):
        GCL_listfiles.append(files)
    

#merging both Files
All = []    
for i in range(0, len(GCL_listfiles)):
    hilus = pd.read_csv(GCL_listfiles[i], index_col = 'Sections')
    name = re.sub(areastring,' ',GCL_listfiles[i])
    hilus.columns.name = name[:-4]    
    All.append(hilus)


GCL_Area = DataFrame(np.empty((14), dtype = np.float), index = range(1,15), columns = ['Nothing'])

for index in All:
   GCL_Area[index.columns.name]= index['GCL Area']
 
del GCL_Area['Nothing']


C57_p30 = []
C57_p16 =[]
C57 = []
SW_p30 = []
SW= []
C57_p16_C_H =[]
C57_p30_C_H =[]

for i in GCL_Area.columns:
    if re.search('C57', i) and re.search('p16_C_H',i):
        C57_p16_C_H.append(i)
    elif re.search('C57', i) and re.search('p16',i):
        C57_p16.append(i)
    elif re.search('C57', i) and re.search('p30_C_H',i):
        C57_p30_C_H.append(i)
    elif re.search('C57', i) and re.search('p30', i):
        C57_p30.append(i)
    elif re.search('C57', i) and re.search('_', i):
        C57.append(i)
    elif re.search('SW', i) and re.search('p30', i):
        SW_p30.append(i)
    else:
       SW.append(i)
        
Groups = [C57_p16_C_H, C57_p30_C_H, C57_p16, C57_p30, C57, SW_p30 ,SW ]
SGroup = ['C57_p16_C_H','C57_p30_C_H','C57_p16','C57_p30','C57', 'SW_p30' ,'SW' ]
Dictionary = dict(zip(SGroup,Groups))

Sorted_Groups =[]
for i in Groups:
    for x in i:
        Sorted_Groups.append(x)

GCL_Area = GCL_Area.reindex(columns=Sorted_Groups)

##GCL_Area
#for i, group  in enumerate(Groups):
#    GCL_Area[SGroup[i]+'_Mean'] = GCL_Area[group].mean(axis =1)
#    GCL_Area[SGroup[i]+'_Stdev'] = GCL_Area[group].std(axis=1)
#    GCL_Area[SGroup[i]+'_Serror'] = GCL_Area[SGroup[i]+'_Stdev']/np.sqrt(len(group))

#
#GCL_Area
GCL_Area=GCL_Area.reindex(columns=Sorted_Groups)   
for i, group  in enumerate(Groups):
    GCL_Area[SGroup[i]+'_Mean'] = GCL_Area[group].mean(axis =1)
    GCL_Area[SGroup[i]+'_Values']= GCL_Area[group].count(axis=1)
    GCL_Area[SGroup[i]+'_Stdev'] = GCL_Area[group].std(axis=1)
    GCL_Area[SGroup[i]+'_Serror'] = GCL_Area[SGroup[i]+'_Stdev']/np.sqrt(GCL_Area[SGroup[i]+'_Values'])

#GCL Area Cornals Vs Horizontals


C57_p30_C_Area =  GCL_Area.ix[1:5,Dictionary['C57_p30_C_H']].sum()
C57_p30_H_Area = GCL_Area.ix[6:10,Dictionary['C57_p30_C_H']].sum()
C57_p16_C_Area =  GCL_Area.ix[1:5,Dictionary['C57_p16_C_H']].sum()
C57_p16_H_Area = GCL_Area.ix[6:10,Dictionary['C57_p16_C_H']].sum()

Table_C_H_Area = Series([C57_p16_C_Area.mean(),C57_p16_H_Area.mean(),C57_p30_C_Area.mean(),C57_p30_H_Area.mean()],index =['C57 P16 Coron','C57 P16 Horiz','C57 P30 Coro', 'C57 P30 Horizo'])

C57_p16_C_Area_Error = C57_p16_C_Area.std()
C57_p16_H_Area_Error = C57_p16_C_Area.std()
C57_p30_C_Area_Error = C57_p30_C_Area.std()
C57_p30_H_Area_Error = C57_p30_C_Area.std()


plt.figure() 
Table_C_H_Area.plot(kind='bar', yerr=[C57_p16_C_Area_Error,C57_p16_H_Area_Error,C57_p30_C_Area_Error,C57_p30_H_Area_Error],color='g')
plt.ylabel('GCL_Area')
plt.xticks(rotation=0)

####
GCLAreaSum = GCL_Area.sum()
TableSW_C57 = Series([GCLAreaSum[Dictionary['C57_p16']].mean(),GCLAreaSum[Dictionary['C57_p30']].mean(),GCLAreaSum[Dictionary['SW_p30']].mean(),GCLAreaSum[Dictionary['C57']].mean(),GCLAreaSum[Dictionary['SW']].mean()], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])
TableSW_C57_Error = Series([GCLAreaSum[Dictionary['C57_p16']].std(),GCLAreaSum[Dictionary['C57_p30']].std(),GCLAreaSum[Dictionary['SW_p30']].std(),GCLAreaSum[Dictionary['C57']].std(),GCLAreaSum[Dictionary['SW']].std()], index =['C57 P16','C57 P30','SW P30','C57 P60','SW'])


plt.figure()   
TableSW_C57.plot(kind='bar',yerr=TableSW_C57_Error,color='y')
plt.ylabel('Density of Prox1 in Hilus')
plt.xticks(rotation=0)





#GCL_Area.to_csv(path+"\Cre_Bax"+areastring+".csv")
def plotFigures(parameter,str1, str2,str3 = None,str4= None):
    ## Modify this part
    global GCL_Area
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
    
            
      
    plt.title('GCL Area') # will set the title of the graph
    plt.xlabel('Section Number' ) #will set the x axis title
    plt.ylabel('GCL Area')    
    plt.legend(loc ='best')   
    plt.xlim(xmax=15)


plotFigures(GCL_Area,'C57_p16','C57_p30','SW_p30','C57')
plotFigures(GCL_Area,'C57_p30','SW_p30')
plotFigures(GCL_Area,'C57_p30','C57')  
plotFigures(GCL_Area,'SW_p30','SW')
plotFigures(GCL_Area, 'C57_p16','C57_p30','C57')
plotFigures(GCL_Area,'C57_p16_C_H','C57_p30_C_H')



##Saving Figures---------------------------------------------------------------------------------
#
#fig.savefig('Figures\\Prox1_Hilar_Cells.png', dpi = 400, bbox_inches = 'tight') 
#fig2.savefig('Figures\\Hilar_Area.png', dpi = 400, bbox_inches = 'tight') 
#fig3.savefig('Figures\\Prox1 Cells_Hilar Area.png', dpi = 400, bbox_inches = 'tight')
#
