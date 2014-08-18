# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 15:33:10 2014

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
path = "C:\Users\KBermudez-Hernandez\Documents\Dropbox\Figures\Figure1 p16 p30 p60 density\Prox_NeuN_stacked_bar_graph\Count_Prox_NeuN\C57"
os.chdir(path)#change directory
#cellstring = '_Hilus_cell_count' # string that indentifies the files with cell count
#areastring = '_Hilus_Area'#string tha identifies fiels with Area

## Files that have cell count
listfiles =[]

for files in os.listdir(path):
    if files.endswith(".xls"): #and re.search(cellstring, files):
        listfiles.append(files)
       
#xls_file = pd.ExcelFile ('CellCounter_C57_10_slide1_section2_Hilus.xls')
#table = xls_file.parse('Sheet1')
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
table = pd.read_table('CellCounter_C57_10_slide1_section2_Hilus.xls')
DF = pd.DataFrame({'ID' : 'CellCounter_C57_10_slide1_section2_Hilus.xls','Prox1_NeuN' : table.Type[table.Type ==1].count() ,
'Prox1' : table.Type[table.Type ==2].count()})
#'On_Top' : table.Type[table.Type ==3].count() ,
#'On_NotSure' : table.Type[table.Type ==4].count()})
 
DF = pd.DataFrame(index= {'CellCounter_C57_10_slide1_section2_Hilus.xls'},columns={'Prox1','Prox_NeuN'})
#'On_Top' : table.Type[table.Type ==3].count() ,
#'On_NotSure' : table.Type[table.Type ==4].count()})
 
##Files that Have Hilus Area
Hilus_listfiles=[]
for files in os.listdir(path):
     if files.endswith(".csv") and  re.search(areastring, files):
        Hilus_listfiles.append(files)