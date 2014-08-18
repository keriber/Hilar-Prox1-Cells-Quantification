# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Program Files\WinPython-32bit-2.7.5.3\settings\.spyder2\.temp.py
"""
import os
import shutil
import os
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import re


dstdir = 'G:\Keria\Quntification_CreBax\DefaultThreshold\SGZ_Files'


path = "F:\Backup Seagate Hardrive\Quantification_C57_SW\Quantification_Default_GCL_H\Hilus_Area"
os.chdir(path)
listfiles =[]
for files in os.listdir(path):
    if re.search('p16',files):
        listfiles.append(files)

#change directory
for files in listfiles:
    path2= path + '\\' + files +'\SGZ'
    for i in os.listdir(path2):
        if re.search('csv',i):
            srcfile = path2+'\\'+i
            shutil.copy(srcfile, dstdir)
