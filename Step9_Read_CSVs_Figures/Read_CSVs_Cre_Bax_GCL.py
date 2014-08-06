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
path = "G:\Keria\Quntification_CreBax\GCL\Area"
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


Negative_Corn = []
Negative_Tam = []
Positive_Corn = []
Positive_Tam = []

for i in GCL_Area.columns:
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

Sorted_Groups =[]
for i in Groups:
    for x in i:
        Sorted_Groups.append(x)

GCL_Area = GCL_Area.reindex(columns=Sorted_Groups)

#GCL_Area
for i, group  in enumerate(Groups):
    GCL_Area[SGroup[i]+'_Mean'] = GCL_Area[group].mean(axis =1)
    GCL_Area[SGroup[i]+'_Stdev'] = GCL_Area[group].std(axis=1)
    GCL_Area[SGroup[i]+'_Serror'] = GCL_Area[SGroup[i]+'_Stdev']/np.sqrt(len(group))


#GCL_Area.to_csv(path+"\Cre_Bax"+areastring+".csv")
def plotFigures(parameter,str1, str2,str3 = None,str4= None):
    ## Modify this part
    global GCL_Area
    global Dictionary
    
    
    dictionary = Dictionary
    plt.figure()   
    plt.plot(parameter.index, parameter[dictionary[str1]], linestyle ='--', color = 'r' )
    plt.errorbar(parameter.index,parameter[str1 + '_Mean'] ,yerr=parameter[str1 + '_Serror'], color = 'r', marker ='o',label = 'Mean_'+ str1 )
    
    plt.plot(parameter.index,parameter[dictionary[str2]], linestyle ='--', color = 'g' )
    plt.errorbar(parameter.index,parameter[str2 + '_Mean'] ,yerr=parameter[str2 + '_Serror'], color = 'g', marker ='o',label = 'Mean_'+ str2 )
    
    if str3 == None:
        print 'No group3'
    else:
        plt.plot(parameter.index,parameter[dictionary[str3]], linestyle ='--', color = 'm' )
        plt.errorbar(parameter.index,parameter[str3 + '_Mean'] ,yerr=parameter[str3 + '_Serror'], color = 'm', marker ='o',label = 'Mean_'+ str3 )
    
    if str4 == None:
        print 'No Group4'        
    else:
        plt.plot(parameter.index,parameter[dictionary[str4]], linestyle ='--', color = 'b' )
        plt.errorbar(parameter.index,parameter[str4 + '_Mean'] ,yerr=parameter[str4 + '_Serror'], color = 'b', marker ='o',label = 'Mean_'+ str4 )
    
            
      
    plt.title('GCL Area') # will set the title of the graph
    plt.xlabel('Section Number' ) #will set the x axis title
    plt.ylabel('GCL Area')    
    plt.legend(loc ='best')   
    plt.xlim(xmax=15)


plotFigures(GCL_Area,'Negative_Corn','Negative_Tam','Positive_Corn','Positive_Tam')


##Saving Figures---------------------------------------------------------------------------------
#
#fig.savefig('Figures\\Prox1_Hilar_Cells.png', dpi = 400, bbox_inches = 'tight') 
#fig2.savefig('Figures\\Hilar_Area.png', dpi = 400, bbox_inches = 'tight') 
#fig3.savefig('Figures\\Prox1 Cells_Hilar Area.png', dpi = 400, bbox_inches = 'tight')
#
