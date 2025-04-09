# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 11:00:21 2025

@author: ame
"""

from stellarTools.mist import mist
import astropy.constants as cst
import stellarTools as st
from stellarTools import geneva as g
import matplotlib.pyplot as plt
import numpy as np
import imf
from matplotlib.colors import LinearSegmentedColormap,rgb_to_hsv,hsv_to_rgb
import time
import astropy.units as u
from tqdm import tqdm

#ùù
m=mist()
#%%

MassStar = 1
age,teff,lum,radius,phase=m.evolutionnaryTrack(MassStar)

fig, ax = plt.subplots(3,5,figsize=(16,8),sharex="col",sharey="row")
plt.subplots_adjust(wspace=0, hspace=0.1)
idxPMS=np.where(phase==-1)[0]
idxMS=np.where(phase==0)[0]
idxEvol=np.where(phase==2)[0]
idxEvol2=np.where((phase==3) | (phase==4) | (phase==5))[0]
idxEvol3=np.where(phase==6)[0]
title=[mist.phaseName(-1),mist.phaseName(0),mist.phaseName(2),
       mist.phaseName(3)+"+"+mist.phaseName(4)+"+"+mist.phaseName(5)
       ,mist.phaseName(6)]
idx=[idxPMS,idxMS,idxEvol,idxEvol2,idxEvol3]

fact=[1e9,1e9,1e9,1e9,1e9]
factSign=["G","G","G","G","G"]
for i in range(5):
    ax[0,i].plot(age[idx[i]]/fact[i],teff[idx[i]])
    ax[1,i].plot(age[idx[i]]/fact[i],lum[idx[i]])
    ax[2,i].plot(age[idx[i]]/fact[i],radius[idx[i]])
    
        #ax[-1,i].set_xscale("log")
    ax[-1,i].set_xlabel(f"Age [{factSign[i]}yr]")
    for j in range(3):
        ax[j,i].margins(x=0) 
        if i==0:
            ylabels=["T$_eff$ [K]","L [L$_\\odot$]",' R [R$_\\odot$]']
            ax[j,i].set_ylabel(ylabels[j])
        if i!=0:
            ax[j,i].spines['left'].set_visible(False)
            ax[j,i].yaxis.set_visible(False)
        if i!=4:
            ax[j,i].spines['right'].set_visible(False)
        
        

    ax[1,i].set_yscale("log")
    ax[2,i].set_yscale("log")   
    ax[0,i].set_yscale("log")   
    #ax[0,i].set_ylim(3000,6000)
    ax[0,i].set_title(title[i])
fig.suptitle(f"MIST Evolutionary track for a {MassStar}M$_\\odot$ star ")
#%%
fig,ax = plt.subplots(figsize=(12,9))
ax.plot(teff,lum,color="k",lw=0.1)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim([1e6,1e3])
ax.set_ylim([1e-3,1e7])

mod=1
ax.scatter(teff[::mod],lum[::mod],s=radius[::mod]*10,c=teff[::mod],marker="o",cmap=st.colortemperature.temperatureColorMapFake,vmin=0, vmax=20000,edgecolor="none",zorder=1)


phase_u=np.unique(phase)
idx=[]
for i in range(len(phase_u)):
    idx.append(np.where(phase==phase_u[i])[0][0])
idx=np.array(idx)
idx2=(idx[1:]+idx[0:-1])//2

idx = np.sort(np.append(idx,idx2))
idx = np.append(idx,-1)

age1 = np.array([0,10e-3,20e-3,40e-3,5,10,11,11.2,11.3,11.4,11.45,11.46,11.462,11.463,11.5])
age1_txt=["  0 yr","10 Myr","20 Myr","40 Myr","5 Gyr","10 Gyr","11 Gyr","11.2 Gyr","11.3 Gyr","11.4 Gyr","11.45 Gyr","11.46 Gyr","11.462 Gyr","11.463 Gyr","11.5 Gyr"]
ha = ["left","left","center"]
ha.extend(["right"]*12)
teff1= np.interp(age1*1e9,age,teff)
lum1= np.interp(age1*1e9,age,lum)
for i in range(len(age1)): 
    plt.scatter(teff1[i],lum1[i],color="k",marker=".")
    plt.text(teff1[i],lum1[i],f"{age1_txt[i]}",zorder=101,fontsize=6,va="bottom",ha=ha[i])
ax.set_xlabel("Teff [K]")
ax.set_ylabel("Lum [L$_\\odot$]")
ax.set_title(f"MIST Evolutionary track for a {MassStar}M$_\\odot$ star ")