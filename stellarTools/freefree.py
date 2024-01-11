# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:21:41 2018

@author: ameillan
"""
import numpy as np


def spectrum(ne,T,wl,nulim=1e99):
    c=3e8
    h=6.626068e-34
    k=1.3806503e-23

    nu=c/wl
    e=np.exp(-(h*nu)/(k*T))

    Nff=5.4e-39*ne**2*e*T**(-0.5)
    Kff=3.7e8*ne**2.*nu**(-3)*(1-e)*T**(-0.5)



    return Nff/Kff
