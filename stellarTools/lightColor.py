# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:40:48 2025

@author: ame
"""

import numpy as np
from matplotlib.colors import LinearSegmentedColormap,rgb_to_hsv,hsv_to_rgb


def _desaturate(col, sfact, vfact=1):
    alpha=None
    if len(col) == 4:
        alpha = col[-1]
        col = col[:-1]
        
    col=rgb_to_hsv(col)
    col[1] *= sfact
    col[2] *= vfact
    col = hsv_to_rgb(col)
    
    if alpha:
        col = np.append(col,alpha)
    return col

def lightColor(wl, flux=None, gamma=0.2, uvColor=[0.3, 0.0 , 0.3,0.1],
                                       irColor=[0.3, 0. , 0.0,0.1]):
    
    wl=np.array(wl)
    if len(wl.shape)==0:
        wl=wl[np.newaxis]
    
    try:
        flux=(flux/np.max(flux))**gamma
    except:
        flux=0*wl+1
        
    WLS  = np.array([0.380e-6,0.440e-6,0.490e-6,0.510e-6,0.580e-6,0.645e-6,0.780e-6])
    COLS = np.array([uvColor,[0.4,0,1,1],[0,0,1,1],[0,1,0,1],[1,1,0,1],[1,0,0,1],irColor])
    
    C = ((wl <= WLS[0])[np.newaxis,:]) * COLS[0][:,np.newaxis]
    
    for iwl in range(len(WLS)-1):
        di = (wl>WLS[iwl]) & (wl<=WLS[iwl+1])
        ai = (wl-WLS[iwl+1]) / (WLS[iwl] - WLS[iwl+1])
        ci = ai[np.newaxis,:] * COLS[iwl][:,np.newaxis] + \
             (1-ai[np.newaxis,:]) * COLS[iwl+1][:,np.newaxis]

        C += di[np.newaxis,:]*ci
        
    C += (wl > WLS[-1])[np.newaxis,:] * COLS[-1][:,np.newaxis]

    flux=np.array([flux,flux,flux,0*flux+1])
    return np.transpose(C*flux)



def lightColorMap(wlmin=0.3e-6,wlmax=0.8e-6,uvColor=[0.63, 0.56, 0.7,1 ],
                  irColor=[0.7 , 0.56, 0.56,1],num=256,sfact=1,vfact=1):
    
    uvColor=_desaturate(uvColor,sfact,vfact)
    irColor=_desaturate(irColor,sfact,vfact)    
    
    wl=np.linspace(wlmin,wlmax,num=num)
    cols=lightColor(wl,uvColor=uvColor,irColor=irColor)
    return LinearSegmentedColormap.from_list("lightColor",cols)

