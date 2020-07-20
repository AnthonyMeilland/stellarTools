# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:08:04 2019

@author: ame
"""

import numpy as np

from stellarTools import mag2Flux

def fluxConverter(fluxin,in_unit,out_unit,wl=None,typ=None,zeropoint=None):
    c=3e8
    #n=len(fluxin)
    if in_unit in ['U','B','V','R','I','J','H','K','L','M','N','Q','Ks',"L'",'Qs','N0','N1','N2','N3','N4','N5','Q0','Q1','Q2','Q3','Q4','Q5']:
        band=in_unit
        in_unit="Mag"

    multi=1.

    #first convert everything to W/m2/m

    if in_unit=='Jy':
        F=fluxin*1e-26*c/wl**2*multi
    elif  in_unit=='W/m2/Hz' :
        F=fluxin*c/wl**2*multi
    elif  in_unit=='W/m2/micron' :
        F=fluxin*1e6*multi
    elif  in_unit=='W/cm2/micron' :
        F=fluxin*1e6*1e4*multi
    elif  in_unit=='W/m2/nm' :
        F=fluxin*1e9*multi
    elif  in_unit=='mW/m2/nm':
        F=fluxin*1e9*1000*multi
    elif  in_unit=='W/m2/m' :
        F=fluxin*multi
    elif  in_unit=='Mag' :
        Fs=mag2Flux(fluxin,band,'W/m2/m',zeropoint=zeropoint,wl=wl,typ=typ)
        F=Fs['f']
        wl=Fs['wl']

    if out_unit=='Jy' :
        fluxout=F*wl**2/c*1e26
    if out_unit=='W/m2/Hz' :
        fluxout=F*wl**2/c
    if out_unit=='W/m2/micron' :
        fluxout=F/1e6
    if out_unit=='W/m2/m' :
        fluxout=F
    if out_unit=='W/m2/nm' :
        fluxout=F/1e9
    if out_unit=='W/cm2/micron' :
        fluxout=F/1e6/1e4

    return {"wl":wl,"f":fluxout}

