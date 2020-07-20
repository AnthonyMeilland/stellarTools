# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:39:30 2014
@author: ame

Interstellar extinction (A)  is taken from :
-Cardelli et al. ApJ 345, 245 for 0.1e-6m<lam<3.333e-6m
-Allen Astrophysical quantities 4th edition pages 527-528 for lam >3.333e-6m.

Bellow 0.1e-6m it is arbitrarely fixed to A(0.1e-6).

wavelength should be in meters!!!
"""
import numpy as np
import math
from scipy import interpolate


_lamIR=np.array([2.2,3.4,5.0,7.0,9.0,9.7,10,12,15,18,20,25,35,60,100,250])

                                         
_Alam_IR3_1=np.array([0.108,0.051,0.027,0.020,0.042,0.059,0.054,0.028,0.015,
                      0.023,0.021,0.014,3.7e-3,2.0e-3,1.2e-3,4.2e-4])
                      
_Alam_IR5_0=np.array([0.125,0.059,0.031,0.023,0.051,0.068,0.063,0.032,0.017,
                      0.027,0.025,0.016,4.2e-3,2.3e-3,1.3e-3,4.9e-4])
                    
_falam_3_1=interpolate.interp1d( _lamIR, _Alam_IR3_1, kind="linear",bounds_error=False)
_falam_5_0=interpolate.interp1d( _lamIR, _Alam_IR5_0, kind="linear",bounds_error=False)

class interstellar_exctinction():
    
    def __init__(self,Av,Rv,lam):

        if type(lam)!=type(np.array([])):        
            if type(lam)!=type([]):
                lam=np.array([lam])
            else:
                lam=np.array(lam)

        Nel= len(lam)
        self.alam=np.zeros(Nel)
        for i in range(Nel):
            x=1./lam[i]
            y=x-1.82
            if (x>=0.004 and x<0.3):                
                alam_3_1= _falam_3_1([lam[i]])[0]
                alam_5_0= _falam_5_0([lam[i]])[0]
                
                print(alam_3_1)
                print(alam_5_0)
                falam=interpolate.interp1d([3.1,5.0],[alam_3_1,alam_5_0], kind="linear",bounds_error=False)
                self.alam[i]=falam([Rv])
                
                
                
        
        
        
        
        
        
        