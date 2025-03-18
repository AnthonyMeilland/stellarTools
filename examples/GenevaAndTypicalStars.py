# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:42:06 2021

@author: Ame
"""

import numpy as np
from stellarTools import geneva as g
from stellarTools import typicalStar
import matplotlib.pyplot as plt



def polyFill(axe,X1,Y1,X2,Y2,color="k",alpha=1,zorder=0):

    XX=np.concatenate([X1,np.flip(X2)])
    YY=np.concatenate([Y1,np.flip(Y2)])
    axe.fill(XX,YY,zorder=zorder,alpha=alpha,color=color)
  

fig,ax=plt.subplots()




zam=g.zeroAgeMainSequence()
w=0
for i,massi in enumerate(zam.Mass):
    if i%2==0:
        track=g.evolutionaryTrack(massi)
        
        L=10**track.data["lg(L)"]
        Teff=10**track.data["lg(Teff)"]
        ax.loglog(Teff,L,color="gray",lw=0.5)
        txt="{0}M$_\\odot$".format(massi)
        ax.text(Teff[w],L[w],txt,size=6,weight="bold",
            bbox=dict(boxstyle='square,pad=0', fc='none', ec='none'),va="top",ha="right")


fam=g.zeroAgeMainSequence(ageIdx=110)
polyFill(ax,zam.Teff,zam.Lum,fam.Teff,fam.Lum,color="k",alpha=0.1)

star=g.genevaStar(1,5e9)
plt.scatter(star.teff,star.lum,marker="X",color="k",s=20)


ax.set_xlim([1e5,3e3])
ax.set_ylim([0.15,3e6])
ax.set_xlabel("T$_{{eff}}$ (K)")
ax.set_ylabel("Lum. (L$_\\odot$)")


SpTypes=["K0V","G0V","F0V","A0V","B5V","B0V","O5V"]
colors=["r","tab:orange","y","g","c","b","purple"]


for i,spTi in enumerate(SpTypes):
    s=typicalStar(spTi)
    ax.scatter(s.Teff,s.Lum,marker="o",color=colors[i],s=10)
    ax.text(s.Teff,s.Lum,spTi+" ",va="bottom",ha="left",color=colors[i],weight="bold")






#FS CMa
L0=10**2.88
Lm=10**(2.88-0.17)
Lp=10**(2.88+0.32)

Teff0=16500
Teffm=16500-80
Teffp=16500+3000

R0=L0**0.5*(5778./16500.)**2


#plt.plot([Teff0,Teff0],[Lm,Lp],color="k")
#plt.plot([Teff0,Teff0],[Lm,Lp],color="k")
#plt.plot([Teffm,Teffp],[L0,L0],color="k")
