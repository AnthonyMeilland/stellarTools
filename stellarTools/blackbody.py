# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 17:49:47 2019

@author: ame
"""

import numpy as np
import os

path = os.path.abspath(__file__)
dir0 = os.path.dirname(path)

mas2rad=np.pi/180/3600/1000.

def blackBody(lam,T):
     #lam in m;
     #result in W/m^3/sr

    c=2.997e8
    h=6.2606896e-34
    k=1.3806504e-23

    B_lam=2*h*c**2./(lam**5.*(np.exp(h*c/(lam*k*T))-1.))

    return B_lam

def blackBodyStar(lam,T,Reto,dist):
     #lam in m;
     #Reto in Ro;
     #dist in pc
     #result en W/m^

    Ro=7e8
    parsec=3.08e16

    R=Reto*Ro
    d=dist*parsec

    print(np.pi*(R/d)**2.)
    F_lam=np.pi*(R/d)**2.*blackBody(lam,T)
    return F_lam

def blackBodyStarAngular(lam,T,diam):
     #lam in m;
     #diam in mas
     #result en W/m^3

    S=np.pi*(diam/2*mas2rad)**2
    print(S)
    F_lam=S*blackBody(lam,T)
    return F_lam