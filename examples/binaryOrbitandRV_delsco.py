# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 11:39:40 2018

@author: ameillan
"""

import numpy as np
import binary 
import matplotlib.pyplot as plt

day = 86400.
yr  = 365.25*day
deg  = np.pi/180.
mas  = deg/3600./1000.

t0=2000.693*yr#;t0=2000.9389d*yr;   2.45176e+06*day
e = 0.94
a = 98.3* mas
T = 10.74*yr
i = 38.0* deg
o = 1.9 * deg
O = 175.2 * deg
v0 = -6.3066559
Ka = 23.692768


time = np.linspace(t0,t0+T,1000)

Coord=binary.binaryProjectedCoordinates(time,t0,e,a,T,i,o,O) / mas



#%% Plotting the projected orbit

fig,ax = plt.subplots(figsize=(7,12))
ax.plot(Coord[0,:],Coord[1,:],color='k')
ax.axis('equal')


ax.scatter(0,0,marker='o',color='k')
ax.set_xlabel('x (mas)')
ax.set_ylabel('y (mas)')
ax.set_xlim([50,-50])
for j in range(11):
    time2 =  (2011+j)*yr
    Coord2=binary.binaryProjectedCoordinates(time2,t0,e,a,T,i,o,O)/ mas
    plt.scatter(Coord2[0],Coord2[1],marker='x',color='b')
    plt.text(Coord2[0]-2,Coord2[1],'{0:0.0f}'.format(2011+j),color='b')
ax.arrow(50,170,0,10,width=1,color='k')
ax.arrow(50,170,10,0,width=1,color='k')
ax.text(45,175,'N',verticalalignment='center',horizontalalignment='center',size=20)
ax.text(55,164,'E',verticalalignment='center',horizontalalignment='center',size=20)


#%% Radial velocity

time = np.linspace(t0-0.1*T,t0+2.1*T,10000)
rv=binary.radialVelocity(time,T,t0,e,o,Ka,v0)
plt.figure()
plt.plot(time/yr,rv)
plt.xlabel('time (yr)')
plt.ylabel('radial velocity (km/s)')










