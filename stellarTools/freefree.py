# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:21:41 2018

@author: ameillan
"""
import numpy as np
import os

path = os.path.abspath(__file__)
dir0 = os.path.dirname(path)


 
def spectrum(nee,T,wl):        
    c=3e8
    h=6.626068e-34
    k=1.3806503e-23
    
    nu=c/wl
    e=np.exp(-(h*nu)/(k*T))
          
    Nff=5.441e-39*nee*e*T**(-0.5)
    Kff=3.65e8*nee**2.*nu**(-3)*(1-e)
          
    return Nff/Kff
