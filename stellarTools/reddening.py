# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:39:30 2014
@author: ame

Interstellar extinction (A)  is taken from :
-Cardelli et al. ApJ 1989 345, 245 for 0.1e-6m<lam<3.333e-6m
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

 



fritz=np.array([[0.419,72.723],[
0.597,39.117],[
0.686,31.411],[
0.837,18.945],[
1.271,8.105],[
2.678,1.663],[
2.934,2.132],[
3.095,2.013],[
3.301,1.663],[
3.961,1.032],[
4.179,0.975],[
5.643,0.853],[
6.918,0.813],[
7.953,0.87],[
8.901,2.784],[
9.291,4.36],[
9.698,4.796],[
10.68,3.005],[
11.7,1.556],[
12.41,1.158],[
15.462,1.18],[
17.12,1.527],[
18.356,1.586],[
20.654,1.336],[
25.186,0.886]])
    
    
def fritz_extinction(lam,Av=0):
    lam=lam*1e6
    
    falam=interpolate.interp1d(np.log10(fritz[:,0]), np.log10(fritz[:,1]),bounds_error=False,fill_value="extrapolate",kind="linear")
    alam=10**falam( np.log10(lam))/48*Av
    return alam







def interstellar_extinction(lam,Av=0,Rv=3.1):

    if type(lam)!=type(np.array([])):        
        if type(lam)!=type([]):
            lam=np.array([lam])
        else:
            lam=np.array(lam)

    lam=lam*1e6
    
    Nel= len(lam)
    alam=np.zeros(Nel)
    for i in range(Nel):
        x=1./lam[i]
        y=x-1.82
        if (x >= 0.004) and (x < 0.3):                
            alam_3_1= _falam_3_1([lam[i]])[0]
            alam_5_0= _falam_5_0([lam[i]])[0]
            
            falam=interpolate.interp1d([3.1,5.0],[alam_3_1,alam_5_0],bounds_error=False,fill_value="extrapolate",kind="linear")
            alam[i]=falam([Rv])*Av
               
        elif (x >= 0.3) & (x < 1.1):
            alam[i]=Av*(0.574*x**1.61-0.527*x**1.61/Rv)
        elif (x >= 1.1) & (x < 3.0):
            alam[i]=Av*(1+0.17699*y-0.50447*y**2-0.02427*y**3+0.72085*y**4+0.01979*y**5-0.77530*y**6+0.32999*y**7+(1.41338*y+2.28305*y**2+1.07233*y**3-5.38434*y**4-0.62251*y**5+5.30260*y**6-2.09002*y**7)/Rv)
        elif (x >= 3.0) & (x < 5.9):
            alam[i]=Av*(1.752-0.316*x-0.104/((x-4.67)**2.+0.341)+(-3.090+1.825*x+1.206/((x-4.62)**2+0.263))/Rv)
        elif (x >= 5.9) & (x < 8.0): 
            alam[i]=Av*(1.752-0.316*x-0.104/((x-4.67)**2.+0.341)-0.04473*(x-5.9)**2-0.009779*(x-5.9)**3+(-3.090+1.825*x+1.206/((x-4.62)**2+0.263)+0.2130*(x-5.9)**2+0.1207*(x-5.9)**3)/Rv)
        elif (x >= 8.0) & (x < 10.):
            alam[i]=Av*(-1.073-0.628*(x-8)+0.137*(x-8)**2-0.070*(x-8)**3+(13.67+4.257*(x-8)-0.420*(x-8)**2+0.374*(x-8)**3)/Rv)
        elif (x >= 10.):
            alam[i]=Av*(-1.073-0.628*(10-8)+0.137*(10-8)**2-0.070*(10-8)**3+(13.67+4.257*(10-8)-0.420*(10-8)**2+0.374*(10-8)**3)/Rv)  # A Verifier
            
    return alam
                
                
   
   
def deredden(lam,F,Av=0,Rv=3.1,useModel=None):
    if useModel==None:
        alam=interstellar_extinction(lam,Av,Rv)
    elif useModel=="Fritz":
        alam=fritz_extinction(lam,Av=Av)
    Fnew=F*10**(0.4*alam)
    return Fnew
        
        
        
        
        
        
        