# -*- coding: utf-8 -*-

import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import special

day = 86400.
yr  = 365.25*day
deg  = np.pi/180.
mas  = deg/3600./1000.


def Rotate_2D(Coord,theta):
    rotMat = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    Coord1 = np.matmul(rotMat,Coord);
    return Coord1

def RotateOrbit(XY_Coord, i, omega, OMEGA):

     Coord3 = XY_Coord
     Coord1 = XY_Coord
     Coord1 = Rotate_2D(XY_Coord,np.pi/2-omega)
     Coord2 = Coord1
     Coord2[0] = Coord1[0] * np.cos(i);
     Coord3 = Rotate_2D(Coord2,-OMEGA);
     return Coord3 

def keplerCoordinates(phase, eccentricity, majorAxis):
    rho = majorAxis * (1 - eccentricity * np.cos(phase));
    
    #rho = majorAxis *(1-eccentricity**2) / (1 + eccentricity * np.cos(phase));
    
    theta = 2*np.arctan(np.tan(phase/2.0) * np.sqrt((1+eccentricity)/(1-eccentricity)));
    X = rho*np.cos(theta);
    Y = rho*np.sin(theta);   
    XY = np.array([X,Y])  
    return XY

def binaryCoordinates(time, eccentricity, majorAxis, period):
    omega = 2*np.pi/period
    order = 20
    phi = omega * time  
    for k in range(1,order):
        phi = phi + 2 * special.jn(float(k),k * eccentricity)/float(k) * np.sin(float(k) * omega * time)
    #phi = (phi-np.pi) % (2*np.pi) + np.pi
    #phi = phi % (2*np.pi) 
    XY = keplerCoordinates(phi,eccentricity,majorAxis)    
    return XY

def binaryProjectedCoordinates(time, t0, eccentricity, majorAxis, period, i, omega, OMEGA):  
    CoordOrbit = binaryCoordinates(time-t0,eccentricity,majorAxis,period)
    CoordP2 = RotateOrbit(CoordOrbit,i,omega,OMEGA)
    return CoordP2


def orbit2Mass(period,majorAxis):
    G=6.673e-11
    omega = 2.0*np.pi/period;
    totalMass = omega**2 * majorAxis**3 / G;
    return totalMass

def radialVelocity(time,T,t0,e,omega,Ka,V0):
    ninterpol=10000
    EEi=np.linspace(0,2*np.pi,ninterpol)
    ti=T/(2*np.pi)*(EEi-e*np.sin(EEi))
    tr=(t0-time) % T
    EE=np.interp(tr,ti,EEi)
    nu=2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(EE/2.))
    return V0-Ka*(np.cos(omega+nu)+e*np.cos(omega))




class rv:
    def __init__(self,t,v,dv=0):
        self.t=t
        self.v=v
        self.dv=dv
        
class sep:
    def __init__(self,t,x,dx,y,dy):
        self.t=t
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
    
class orbit(object):
    def __init__(self,**kwargs):
        self.RV=[]
        self.sep=[]
        self.e = 0
        self.a = 1 * mas
        self.T = 1 * yr
        self.i = 0 * deg
        self.o = 0 * deg
        self.O = 0 * deg
        self.v0 = 0
        self.Ka = 0
        self.setParams(**kwargs)
        
    def setParams(self,**kwargs):
        self.__dict__.update(kwargs)
    
    def addRv(self,t,v,dv=0):       
        self.RV.append(rv(t,v,dv))
    
    def addSep(self,t,x,dx,y,dy) :   
         self.sep.append(sep(t,x,dx,y,dy))
         
    
    def plotOrbit(self):
        npts=1000
        plt.figure()
        time = np.linspace(self.t0,self.t0+self.T,npts)
        Coord=self.compute(time)
        plt.plot(Coord[0],Coord[1],color='k')
        plt.axis('equal')
        plt.scatter(0,0,marker='+',color='k')
        plt.xlabel('x (mas)')
        plt.ylabel('y (mas)')
        
        minx=np.min(Coord[0])
        maxx=np.max(Coord[0])
        #miny=np.min(Coord[1])
        maxy=np.max(Coord[1])        
        plt.xlim([maxx,minx])
        
        plt.arrow(0.9*maxx,0.9*maxy,0,0.02*maxy,width=1,color='k')
        plt.arrow(0.9*maxx,0.9*maxy,0.02*maxy,0,width=1,color='k')
        plt.text(0.7*maxx,0.92*maxy,'N',verticalalignment='center',horizontalalignment='center',size=20)
        plt.text(0.97*maxx,0.87*maxy,'E',verticalalignment='center',horizontalalignment='center',size=20)
        plt.show()


    
    def compute(self,time):
        return binaryProjectedCoordinates(time,self.t0,self.e,self.a,self.T,self.i,self.o,self.O) / mas


