# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:20:05 2017

@author: ame
"""

from astropy import units as u
import numpy as np


def filterConv(band,system="Johnson"):
    if system=="Johnson":
        return u.spectral_density(JohnsonDef[band].lam)


class photoBand:
    def __init__ (self,name,lam,F0):
        self.name=name
        self.lam=lam
        self.F0=F0
        
JohnsonDef={"U" : photoBand("U",0.36*u.micron,1823*u.Jy),
            "B" : photoBand("B",0.43*u.micron,4130*u.Jy),
            "V" : photoBand("V",0.55*u.micron,3781*u.Jy),
            "R" : photoBand("R",0.70*u.micron,2941*u.Jy),
            "I" : photoBand("I",0.90*u.micron,2635*u.Jy),
            "J" : photoBand("J",1.25*u.micron,1603*u.Jy),
            "H" : photoBand("H",1.60*u.micron,1075*u.Jy),
            "K" : photoBand("K",2.22*u.micron, 667*u.Jy),
            "L" : photoBand("L",3.54*u.micron, 288*u.Jy),
            "M" : photoBand("M",4.80*u.micron, 170*u.Jy),
            "N" : photoBand("N",10.*u.micron,  36*u.Jy)}
   

photomConvTable={"Johnson":JohnsonDef}
 
def MagToFlx(mag,outunit,band,system="Johnson"):
    return (10**(-mag/2.5)*photomConvTable[system][band].F0).to(outunit,equivalencies=filterConv(band,system))
     

def FlxToMag(flx,band,system="Johnson"):
    return -2.5*np.log10(flx.to(u.Jy,equivalencies=filterConv(band,system))/photomConvTable[system][band].F0)
    
    

