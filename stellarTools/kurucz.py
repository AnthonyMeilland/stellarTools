# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 16:01:39 2013

@author: ame
"""
import numpy as np
import os

path = os.path.abspath(__file__)
dir0 = os.path.dirname(path)

mas2rad=np.pi/180/3600/1000.

class star:

    def __init__(self,RstarOrDiam,Teff,geff,distance=0,lam=0):

        if (geff>5):
            print("Warning : no model for geff>5. geff=5 used instead")
            geff=5
        if (geff<0):
            print("Warning : no model for geff<0. geff=0 used instead")
            geff=0
        if (Teff>=50000):
            print("Warning : no model for Teff>50000. Teff=50000 used instead")
            Teff=49999
        if (Teff<3500):
            print("Warning : no model for Teff<3500. Teff=3500 used instead")
            Teff=3500



        dir=dir0+'/kurucz_data/'
        files_raw=[f for f in os.listdir(dir) if f.find('kp00_')!=-1]
        Tkur_raw=[float(f[5:-4]) for f in files_raw]

        nkur=len(Tkur_raw)
        #"Sorting files in increasing values of Teff. This is normally useless anyway..."
        s=sorted(range(nkur),key=lambda k:Tkur_raw[k])
        Tkur=[Tkur_raw[i] for i in s]
        files=[dir+files_raw[i] for i in s]

        iT0=[i for i in range(nkur) if Teff>=Tkur[i]][-1]
        iT1=iT0+1

        T0=Tkur[iT0]
        T1=Tkur[iT1]

        PT0=(T1-Teff)/(T1-T0)
        PT1=(Teff-T0)/(T1-T0)

        ig0=int(geff*2+1)
        ig1=ig0+1

        g0=int(geff*2)/2.0
        g1=g0+0.5

        Pg0=(g1-geff)/(g1-g0)
        Pg1=(geff-g0)/(g1-g0)

        arr0=np.loadtxt(files[iT0])
        arr1=np.loadtxt(files[iT1])


        self.wl=arr0[:,0]/1e10

        A00=arr0[:,ig0]
        A10=arr1[:,ig0]

        if (g0<5):
            A01=arr0[:,ig1]
            A0=A00*Pg0+A01*Pg1
            A11=arr1[:,ig1]
            A1=A10*Pg0+A11*Pg1
        else:
            A0=A00
            A1=A10

        A=A0*PT0+A1*PT1

        d_km=distance*3.08e13
        R_km=RstarOrDiam*7e5
        "10x = conversion erg/s/cm^2/A in W/m2/micron"
        #if distance=0 we assume Rstar is in fact the angular diameter
        if distance==0:
            ratio=10*(mas2rad*RstarOrDiam/2)**2
        else:
            ratio=10.*(R_km/d_km)**2



        self.f=A*ratio


