# -*- coding: utf-8 -*-
"""
*******************************************************************************

Created on Tue Nov 26 02:17:21 2013
@author: Anthony Meilland

This module contains the class typicalStar that return "standard" stellar para-
meters for a given spectral class. The Teff, Radius, and Mass are taken from
Allen's Astrophysical Quantities.The Luminosity is computed from the Radius and
Teff and the critical velocity from using the Radius and the Mass.

You first need to instentiate the class with a spectral class :
    s=typicalStar('B3V')

Then you can access to the corresponding stellar parameters :
    s.Teff    # The effective temperature (in K)
    s.Radius  # The stelllar radius (in Ro)
    s.Mass    # The Stellar Mass (in Mo)
    s.Lum     # The Stellar Luminosity (in Lo)
    s.Vcrit   # The roche-lobe critical velocity (in km/s)

You can also print all the parameters simultaneously using the print function:
    print(s)

Finally, you can create load an interpolated kurucz model using the kurucz.star
module for this set of stellar parameters:
    sed=s.getKuruczModel(distance=100)  # the distance is in parsecs.


To do / Comments :
geff still needs to be computed (for kurucz model we use geff=4.5)
*******************************************************************************
"""

import numpy as np
import math
from scipy import interpolate
from stellarTools import kurucz as kz

spTypes_base=np.array(['O','B','A','F','G','K','M'])
class typicalStar:

    def __init__(self,spClass):
        self.Teff=0
        self.Radius=0
        self.Mass=0
        self.Vcrit=0
        self.spClass=spClass
        self.spType_num=-1
        self.class_num=-1
        l=len(spClass)
        if (l>0):
            i=np.where(spTypes_base==spClass[0])[0]
            if (len(i)>0):
                self.spType_num=i[0]*10
                if (l>1):
                    decal=1
                    try:
                        self.spType_num+=float(spClass[1:4])
                        decal+=3
                    except:
                       try:
                           self.spType_num+=float(spClass[1])
                           decal+=1
                       except:
                           pass

                    compl=spClass[decal:]

                    if (compl.find('V')==0):
                        self.class_num=5
                    elif (compl.find('IV')==0):
                        self.class_num=4.
                    elif (compl.find('III')==0):
                        self.class_num=3.
                    elif (compl.find('II')==0):
                        self.class_num=2.
                    elif (compl.find('I')==0):
                        self.class_num=1

                    if (compl.find('/')!=-1):
                        self.class_num+=0.5

        if (self.spType_num!=-1):
            x=np.array([0,5,9,10,12,15,18,20,22,25,30,32,35,38,40,42,45,48,50,52,55,60,62,65,69])
            y=np.array([50000,42000,34000,30000,20900,15200,11400,9790,9000,8180,7300,7000,6650,6250,5940,5790,5560,5310,5150,4830,4410,3840,3520,3170,2500])
            fTeff = interpolate.interp1d(x, y, kind="linear",bounds_error=False,fill_value="extrapolate")
            self.Teff=fTeff([self.spType_num])[0]
        else:
            self.Teff=0



        if (self.class_num!=-1):
            x=np.array([5 ,6 ,8 ,10,15,20,25,30,35 ,40 ,45 ,50 ,55 ,60 ,62])
            yr=np.array([30,25,20,30,50,60,60,80,100,120,150,200,400,500,800])
            ym=np.array([70,40,28,28,20,16,13,12,10,10,12,13,13,13,19])
            fRclassI= interpolate.interp1d(x, yr, kind="linear",bounds_error=False,fill_value="extrapolate")
            fMclassI= interpolate.interp1d(x, ym, kind="linear",bounds_error=False,fill_value="extrapolate")
            RadiusI=fRclassI([self.spType_num])[0]
            MassI=fMclassI([self.spType_num])[0]

            x=np.array([10,15,20,40,45,50,55,60])
            yr=np.array([15,8 ,5 ,6 ,10,15,25,40])
            ym=np.array([20,7 ,4 ,1 ,1.1,1.1,1.2,1.2])
            fRclassIII= interpolate.interp1d(x, yr, kind="linear",bounds_error=False,fill_value="extrapolate")
            fMclassIII= interpolate.interp1d(x, ym, kind="linear",bounds_error=False,fill_value="extrapolate")
            RadiusIII=fRclassIII([self.spType_num])[0]
            MassIII=fMclassIII([self.spType_num])[0]

            x=np.array([3,5,6,8,10,13,15,18,20,25,30,35,40,45,50,55,60,62,65,68])
            yr=np.array([15,12,10,8.5,7.4,4.8,3.9,3.0,2.4,1.7,1.5,1.3,1.1,0.92,0.85,0.72,0.6,0.5,0.27,0.1])
            ym=np.array([120,60,37,23,17.5,7.6,5.9,3.8,2.9,2.0,1.6,1.4,1.05,0.92,0.79,0.67,0.51,0.4,0.21,0.06])
            fRclassV= interpolate.interp1d(x, yr, kind="linear",bounds_error=False,fill_value=0)
            fMclassV= interpolate.interp1d(x, ym, kind="linear",bounds_error=False,fill_value=0)
            RadiusV=fRclassV([self.spType_num])[0]
            MassV=fMclassV([self.spType_num])[0]
            x=np.array([1,3,5])
            Radii=np.array([RadiusI,RadiusIII,RadiusV])
            Masses=np.array([MassI,MassIII,MassV])
            fRadius=interpolate.interp1d(x, Radii, kind="linear",bounds_error=False,fill_value="extrapolate")
            fMass=interpolate.interp1d(x, Masses, kind="linear",bounds_error=False,fill_value="extrapolate")
            self.Radius=fRadius([self.class_num])[0]
            self.Mass=fMass([self.class_num])[0]
        else:
            self.Radius=0


        self.Lum=(self.Teff/5750)**4*self.Radius**2

        try:
            self.Vcrit=356.*math.sqrt(self.Mass/self.Radius)
        except:
            pass
    def __str__(self):
        text="Typical {0} star \nTeff = {1:.0f}K\nRadius = {2:.2f}Ro\nMass = {3:.2f}Mo\nLuminosity = {4:.2f}Lo\nVcrit = {5:.0f}km/s".format(self.spClass,self.Teff,self.Radius,self.Mass,self.Lum,self.Vcrit)
        return text

    def getKuruczModel(self,distance=1):
        return kz.star(self.Radius,self.Teff,4.5,distance)
