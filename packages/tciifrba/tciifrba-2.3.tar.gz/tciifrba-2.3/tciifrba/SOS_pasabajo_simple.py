#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 23:14:49 2019

@author: mariano
"""

# Módulos para Jupyter

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
#%%  Inicialización de librerías
# Setup inline graphics: Esto lo hacemos para que el tamaño de la salida, 
# sea un poco más adecuada al tamaño del documento
mpl.rcParams['figure.figsize'] = (10,10)

#%% Esto tiene que ver con cuestiones de presentación de los gráficos,
# NO ES IMPORTANTE
fig_sz_x = 14
fig_sz_y = 13
fig_dpi = 80 # dpi

fig_font_family = 'Arial'
fig_font_size = 16

plt.rcParams.update({'font.size':fig_font_size})
plt.rcParams.update({'font.family':fig_font_family})

# módulo de SciPy
from scipy import signal as sig


# un módulo adaptado a mis necesidades
from tciifrba import analyze_sys, pretty_print_bicuad_omegayq
        
all_sos = []
all_values = [2, 1,5,10]

for ii in all_values:
    
    wo = ii
    qq = np.sqrt(2)/2 
    
    num = np.array([wo**2]) 
    den = np.array([1, wo/qq, wo**2])
    
    pretty_print_bicuad_omegayq(num,den)

    mi_sos = sig.TransferFunction(num,den)

    all_sos += [mi_sos]
    
plt.close('all')
analyze_sys(all_sos, sys_name=all_values)