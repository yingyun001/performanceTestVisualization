#!/usr/bin/env python
# encoding: utf-8
import os
parameterFixed = ['DB', 'QD']
parameterFixed_DB_values = ['4K', '16K', '1M', '4M', '8M']
parameterFixed_QD_values = ['1', '4', '16', '64']
index = [2, 3, 4, 5, 6, 7, 8, 9]
for pf in parameterFixed:
    if pf == 'DB':
        parameterFixedValues = parameterFixed_DB_values
    else:
        parameterFixedValues = parameterFixed_QD_values
    for pfv in parameterFixedValues:
        for i in index:
            os.system("python readDataFromCSV.py %s %s %s %s" % ("./画图/AE/4cpu16g", pf, pfv, i))
            os.system("python readDataFromCSV.py %s %s %s %s" % ("./画图/AEQ/1cpu1g", pf, pfv, i))
            os.system("python readDataFromCSV.py %s %s %s %s" % ("./画图/AEQ/2cpu4g", pf, pfv, i))
            os.system("python readDataFromCSV.py %s %s %s %s" % ("./画图/QE/8cpu8g", pf, pfv, i))

