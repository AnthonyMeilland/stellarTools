# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 10:49:40 2019

@author: ame
"""

import numpy as np
import scipy
from scipy import interpolate


def udisk(lam=None, B=None, V=None, D=None, size=1):
    nkeys=(lam!=None)+(B!=None)+(V!=None)+(D!=None)
    
    #print (nkeys)
    if np.shape(lam)==():
        if lam!=None:
            lam=np.array([lam])
    if np.shape(D)==():
        if D!=None:
            D=np.array([D])        
    if np.shape(B)==():
        if B!=None:
            B=np.array([B])        
    if np.shape(V)==():
        if V!=None:
            V=np.array([V])    
    if False:
        print("This function is meant to be used with 3 parameters")
    else:
        if np.shape(lam)==():
            lam=np.ndarray(np.shape(B))
            X=(np.arange(3830*size)+1.)/1000.
            Y=2*np.abs((scipy.special.jn(1,X)/X))
            for i in range(np.size(D)):
                Xd=X/3.83*D[i]*B[i]/250.
                f=interpolate.interp1d(Y,Xd,fill_value='extrapolate')
                lam[i]=f(V[i])
            return lam
        elif np.shape(B)==():
            B=np.ndarray(np.shape(lam))
            X=(np.arange(3830*size)+1.)/1000.
            Y=2*np.abs((scipy.special.jn(1,X)/X))
            for i in range(np.size(D)):
                Xd=X/3.83*250*lam[i]/D[i]
                f=interpolate.interp1d(Y,Xd,fill_value='extrapolate')
                B[i]=f(V[i])
            return B
        
        elif np.shape(V)==():
            V=2*np.abs(scipy.special.jn(1,3.83/250.*D*B/lam)/(3.83/250.*D*B/lam))
            return V
        else: #D==None
            D=np.ndarray(np.shape(lam))
            X=(np.arange(3830*size)+1.)/1000.
            Y=2*np.abs((scipy.special.jn(1,X)/X))
            for i in range(np.size(B)):
                Xd=X/3.83*250.*lam[i]/B[i]
                f=interpolate.interp1d(Y,Xd,fill_value='extrapolate')
                D[i]=f(V[i])
            return D
        
        