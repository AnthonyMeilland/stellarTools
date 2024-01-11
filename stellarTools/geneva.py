# -*- coding: utf-8 -*-
"""
*******************************************************************************

Created on Thu Jan 28 09:54:52 2021

@author: Anthony Meilland

This module contains the classes with extracted from the evolutionary tracks  
from the Geneva stellar evolution code found at on their website
https://www.unige.ch/sciences/astro/evolution/en/database/file-formats


The points have been normalised for each model:

1: ZAMS
2-84: H burning
85: minimum of Teff on the MS
86-109: H burning
110: Turn-off
111-189: HRD crossing and/or pre-He-burning core contraction
190: beginning of He burning
191-209: He burning
210-350: loop (if any)
351-369: He burning
370: core He exhaustion
371-400: C burning



List of classes:
    evolutionnaryTrack: interpolate between evolutionnary tracks for a given initial mass
    zeroAgeMainSequence : 

"""

import numpy as np
import math
from scipy import interpolate
from stellarTools import kurucz as kz
import os
from astropy.table import QTable
from astropy.io import ascii
import astropy.units as u

def _readGenevaFile(file):
    f=open(file)
    colnames=f.readline().split()
    units=f.readline().split()
    data=f.read()
    f.close()
    data=[di.split() for di in data.split("\n")][1:]
    ldi=np.array([len(di) for di in data])
    idxEnd=np.where(ldi==0)[0][0]
    data=np.array(data[:idxEnd],dtype=float)
    return units,colnames,data

path = os.path.abspath(__file__)
dir0 = os.path.dirname(path)
dirmodel=dir0+"/geneva_data/"


def _listFiles():
    files=np.array([f for f in os.listdir(dirmodel) if (".dat" in f and "V0" in f)])
    masses=np.array([f.split("Z")[0][1:].replace("p",".") for f in files]).astype(float)
    idx=np.argsort(masses)     
    files=files[idx]
    masses=masses[idx]
    return masses,files






class populationAge:
    def __init__(self,age):
        zam=zeroAgeMainSequence()
        self.lum=np.ndarray(len(zam.Mass))
        self.radius=np.ndarray(len(zam.Mass))
        self.teff=np.ndarray(len(zam.Mass))   
        
        for i,massi in enumerate(zam.Mass):
            si=genevaStar(massi,age)
            self.lum[i]=si.lum
            self.radius[i]=si.radius            
            self.teff[i]=si.teff            


class genevaStar:
    
    def __init__(self,mass,age=0):
        self.track=evolutionaryTrack(mass)
        
         
        self.lum=np.interp(age,self.track.data["time"],self.track.lum)
        self.radius=np.interp(age,self.track.data["time"],self.track.radius)
        self.teff= np.interp(age,self.track.data["time"],self.track.teff)       




class evolutionaryTrack:
    
    def __init__(self,Mass):
        masses,files=_listFiles()
        
        if Mass<masses[0] or Mass>masses[-1]:
            print("Error mass outside of {0}-{1}Mo range".format(masses[0],masses[-1]))
            return

        idx1=np.where(masses-Mass >=0)[0][0]      
        dM=masses[idx1]-masses[idx1-1]    
        self.p0=(masses[idx1]-Mass)/dM
        
        self.f1=files[idx1]
        self.f0=files[idx1-1]
              
        units,colnames,data0=_readGenevaFile(dirmodel+self.f0)
        units,colnames,data1=_readGenevaFile(dirmodel+self.f1)
        
        ncol=len(colnames)
        #nrow=np.shape(data0)[1]
        self.data0={}
        self.data1={} 
        self.data={}         
        for i in range(ncol):
            self.data0[colnames[i]]=data0[:,i]
            self.data1[colnames[i]]=data1[:,i]        
            self.data[colnames[i]]=data0[:,i]*self.p0+data1[:,i]*(1-self.p0)
 
        self.mass=Mass
        self.teff=10**self.data["lg(Teff)"]
        self.lum=10**self.data["lg(L)"] 
        self.radius=self.lum**0.5*(5778/self.teff)**2
       
        
        
        
        
class zeroAgeMainSequence:
    
    def __init__(self,mass=None,lum=None,radius=None,teff=None,ageIdx=0):
        self.Mass0,files=_listFiles()
        
        self.Lum0=[]
        self.Teff0=[]

        for massi in self.Mass0:

            ei=evolutionaryTrack(massi)            
            self.Lum0.append(10**ei.data["lg(L)"][ageIdx])
            self.Teff0.append(10**ei.data["lg(Teff)"][ageIdx])
            
       
        self.Mass0=np.array(self.Mass0)
        self.Lum0=np.array(self.Lum0)
        self.Teff0=np.array(self.Teff0)
        self.Radius0=self.Lum0**0.5*(5778./self.Teff0)**2
        
        doInterp=True
        if mass!=None:
            x0= self.Mass0
            x=mass
        elif lum!=None:
            x0= self.Lum0
            x=lum
        elif radius!=None:
            x0= self.Radius0
            x=radius
        elif teff!=None:
            x0= self.Teff0
            x=teff   
        else:
            doInterp=False
            
        if doInterp==True:
            fmass   =interpolate.interp1d(x0, self.Mass0, kind="linear",bounds_error=False,fill_value=0)
            flum    =interpolate.interp1d(x0, self.Lum0, kind="linear",bounds_error=False,fill_value=0)
            fradius =interpolate.interp1d(x0, self.Radius0, kind="linear",bounds_error=False,fill_value=0)
            fteff   =interpolate.interp1d(x0, self.Teff0, kind="linear",bounds_error=False,fill_value=0)
        
            self.Mass=fmass(x)
            self.Lum=flum(x)        
            self.Teff=fteff(x)    
            self.Radius=fradius(x)        
        else:
            self.Mass=self.Mass0
            self.Lum=self.Lum0
            self.Teff=self.Teff0
            self.Radius=self.Radius0
        
        