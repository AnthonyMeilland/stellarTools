# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:42:06 2021

@author: Ame
"""

from stellarTools import geneva as g
import matplotlib.pyplot as plt
import numpy as np


fig,ax=plt.subplots()

# plot evolutionnary paths from genova models every modulo
modulo=1 # used to reduce the number of paths plotted 
zam=g.zeroAgeMainSequence()
for i,massi in enumerate(zam.Mass):
    if i%modulo==0:
        track=g.evolutionaryTrack(massi)
        ax.loglog(track.teff,track.lum,color="gray",lw=0.5)
        txt="{0}M$_\\odot$".format(massi)
        ax.text(track.teff[0],track.lum[0],txt,size=6,weight="bold",
            bbox=dict(boxstyle='square,pad=0', fc='none', ec='none'),va="top",ha="right")

fam=g.zeroAgeMainSequence(ageIdx=85)#end of main-sequence = index 85 for all star (see geneva grid)

plt.plot(zam.Teff,zam.Lum,color="b",label="Zero Age Main Sequence")# plot zero-age main-sequence
plt.plot(fam.Teff,fam.Lum,color="g",label="end of Main Sequence")# plot end of main-sequence

ax.set_xlim([1e5,3e3])
ax.set_ylim([0.15,3e6])
ax.set_xlabel("T$_{{eff}}$ (K)")
ax.set_ylabel("Lum. (L$_\\odot$)")

#%%
# Add your Star
MyRstar = 3.5
MyTeff = 21800
MyLum  = (MyTeff/5777)**4*MyRstar**2

#Getting mass of star based on Teff and Lum considering that the object is on the MS
MyMass=g.fullGrid().getMainSequenceMass(MyTeff,MyLum)
track=g.evolutionaryTrack(MyMass)

MyAge = np.interp(MyLum,track.lum,track.age)/1e6

ax.loglog(track.teff,track.lum,color="r",lw=0.5,alpha=0.5)
plt.scatter(MyTeff,MyLum,marker=".",s=50,label=f"FS CMa (M$_\\star$={MyMass:.1f}M$_\\odot$, Age={MyAge:.1f}Myr)",color="r")

fig.legend()


#%%
Teff_min = 21500
Teff_max = 22100
Rstar_min = 2.6
Rstar_max = 5.1

Lum_min = (Teff_min/5777)**4*Rstar_min**2
Lum_max = (Teff_max/5777)**4*Rstar_max**2

ax.plot([MyTeff,MyTeff],[Lum_min,Lum_max],color="r")
ax.plot([Teff_min,Teff_max],[MyLum,MyLum],color="r")
