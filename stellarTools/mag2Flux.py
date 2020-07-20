# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:55:28 2019

@author: ame
"""
import numpy as np

def mag2Flux(mag,band,unit,struct=True,typ="Johnson",zeropoint=None,wl=None):

    c=3e8

    if band=="Ks":
        typ="2MASS"
    elif band in ['Qs','N0','N1','N2','N3','N4','N5','Q0','Q1','Q2','Q3','Q4','Q5']:
        typ="MERLIN"
    elif band=="G":
        typ="GAIA"

    if zeropoint and wl:
        F=1.*zeropoint*10**(-mag/2.5)
    else:

        if typ=="Johnson":
            Bands=np.array(['U','B','V','R','I','J','H','K','L','M','N','Q'])
            wls=np.array([.36,.44,.55,.71,.97,1.25,1.6,2.22,3.54,4.8,10.6,21.])*1e-6
            F0=np.array([1823,4130,3781,2941,2635,1603,1075,667,288,170,36,9.4])
        elif typ=="2MASS":
            Bands=np.array(['J','H','Ks'])
            wls=np.array([1.235,1.662,2.159])*1e-6
            F0=np.array([1594,1024,666.7])
        elif typ== 'UKIRT':
            Bands=np.array(['V','I','J','H','K','L',"L'",'M','N','Q'])
            wls=np.array([0.5556,0.9,1.25,1.65,2.2,3.45,3.8,4.8,10.1,20])*1e-6
            F0=np.array([3540,2250,1600,1020,657,290,252,163,39.8,10.4])
        elif typ=='MIRLIN':
            Bands=np.array(['K','M','N0','N1','N2','N3','N4','N5','N','Qs','Q0','Q1','Q2','Q3','Q4','Q5'])
            wls=np.array([2.2,4.68,7.91,8.81,9.69,10.27,11.7,12.49,10.79,17.9,17.2,17.93,18.64,20.81,22.81,24.48])*1e-6
            F0=np.array([650,165,60.9,49.4,41.1,36.7,28.5,25.1,33.4,12.4,13.4,12.3,11.4,9.2,7.7,6.7])
        elif typ=='GAIA':
            Bands=np.array(['G'])
            wls=np.array([0.5857])*1e-6
            F0=np.array([2861])

        i=np.where(Bands==band)[0]
        if len(i)!=0:
            i=i[0]
            F=F0[i]*10**(-mag/2.5)
            wl=wls[i]
        else:
            print("Error could not find band {0}".format(band))
            return np.nan

    if unit=='W/m2/Hz':
        F=F*1e-26
    if unit=='W/m2/m':
        F=F*1e-26*c/wl**2
    if unit=='W/m2/micron':
        F=F*1e-26*c/wl**2/1e6
    if unit=='W/cm2/micron':
        F=F*1e-26*c/wl**2/1e6/1e4


    if struct:
        return {"wl":wl,"f":F}
    else:
        return f
