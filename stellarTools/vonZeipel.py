# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:50:57 2018

@author: ame
"""
import numpy as np
from scipy.interpolate import interp1d
import os

path = os.path.abspath(__file__)
dir0 = os.path.dirname(path)


class vonZeipel:
    def __init__(self,v=None,omega=None,flattening=None):
        self.v= None
        self.omega = None
        self.flattening = None
        f=dir0+"/misc_data/vrot.dat"
        fo=open(f,'r')
        d=fo.read()

        d.split()
        d2=d.split()
        d3=np.array(d2)
        d4=np.reshape(d3,[1000,3])
        d4=d4.astype(float)
        self._tab_v=d4[:,2]
        self._tab_omega=d4[:,0]
        self._tab_flattening=d4[:,1]
        self.f_omega_v   = interp1d(self._tab_v, self._tab_omega,fill_value= "extrapolate",bounds_error=None)
        self.f_v_omega   = interp1d(self._tab_omega,self._tab_v,fill_value= "extrapolate",bounds_error=None)      
        self.f_flattening_v     = interp1d(self._tab_v, self._tab_flattening,fill_value= "extrapolate",bounds_error=None)
        self.f_v_flattening     = interp1d( self._tab_flattening,self._tab_v,fill_value= "extrapolate",bounds_error=None)        
        self.f_flattening_omega = interp1d(self._tab_omega,self._tab_flattening,fill_value= "extrapolate",bounds_error=None) 
        self.f_omega_flattening = interp1d(self._tab_flattening,self._tab_omega,fill_value= "extrapolate",bounds_error=None) 
     
        
        if v:
            self.setV(v)
        if omega:
            self.setOmega(omega)
        if flattening:
            self.setFlattening(flattening)
    
    def setV(self,v):
        self.v = v
        self.omega = self.f_omega_v(v)
        self.flattening = self.f_flattening_v(v)
        
    def setOmega(self,omega):
        self.omega = omega
        self.v = self.f.v_omega(omega)
        self.flattening = self.f_flattening_omega(omega)
 
    def setFlattening(self,flattening):
        self.flattening = flattening
        self.v = self.f_v_flattening(flattening)
        self.omega = self.f_omega_flattening(flattening)

           
    def __str__(self):
        text="Von Zeipel model : \n v/v_c ={0} \n omega/omga_c = {1} \n Req/Rpole = {2}".format(self.v,self.omega,self.flattening)
        return text