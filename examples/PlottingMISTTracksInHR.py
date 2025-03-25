# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 07:16:05 2025

@author: ame
"""

import astropy.constants as cst
import stellarTools as st
from stellarTools.mist import mist
import matplotlib.pyplot as plt
import numpy as np
import imf
import matplotlib.cm as cm
import matplotlib.colors as colors
import time
import astropy.units as u
#%%
m=mist()
#%%
fig,ax=plt.subplots(figsize=(12,8))
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim([1e6,1e3])
ax.set_ylim([1e-4,1e7])
ax.set_xlabel("T$_{{eff}}$ (K)")
ax.set_ylabel("Lum. (L$_\\odot$)")


masses=m.grid_mass



log_masses=np.log10(masses)
def colmap(cmap,x,x_all):
    y = (x-x_all.min())/(x_all.max()-x_all.min())
    return cmap(y)

cmap = cm.jet
icol=np.linspace(0,1,num=256)
cols = cmap(icol)
cols*=0.8
cmap2=colors.LinearSegmentedColormap.from_list("bob",cols)



cols = colmap(cmap2,log_masses,log_masses)

for i,massi in enumerate(masses):
    if i % 1 == 0:
        
        age,teff,lum,radius,phase=m.evolutionnaryTrack(massi)
        idx=np.where(phase!=-1)[0] # removing prem-main sequence phase
        ax.plot(teff[idx],lum[idx],alpha=0.5,lw=0.5,color=cols[i,:])
        
        if massi<1:
            txt="{0:.2f}M$_\\odot$".format(massi)
        elif massi<10:
            txt="{0:.1f}M$_\\odot$".format(massi)      
        else:
            txt="{0:.0f}M$_\\odot$".format(massi)   
        if i % 15 == 0:
            ax.text(teff[idx[0]],lum[idx[0]],txt,size=7,weight="normal",
                bbox=dict(boxstyle='square,pad=0', fc="none", ec="none"),va="top",ha="right",color=cols[i,:]*0.6)
            ax.scatter(teff[idx[0]],lum[idx[0]],alpha=0.5,lw=0.2,color=cols[i,:],marker="*")
        

norm = colors.LogNorm(vmin=masses.min(), vmax=masses.max())
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap2),ax=ax, label="Masses [M$_\\odot$]")

age,teff,lum,radius,phase=m.evolutionnaryTrack(1)
idx=np.where(phase!=-1)[0]
cb=ax.plot(teff[idx],lum[idx],color="k",label="Sun",lw=2)
ax.legend()
ax.set_title(f"MIST Evolutionnary tracks from {masses[0]:.2f} to {masses[-1]:.0f} M$_\\odot$ (without PMS)")

#%%

