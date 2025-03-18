import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import stellarTools as st

#%% Creating a typical star SED

Rstar = 1
Teff = 5777
geff = 5
dist = 1 #pc

star=st.kurucz.star(Rstar,Teff,geff,dist)
wls=star.wl
f = star.f

wlim=np.array([3e-7,10e-6])

idx=np.where((wls>=wlim[0]) & (wls<=wlim[1]))[0]
wls=wls[idx]
f=f[idx]

#%% plotting the SED with real color map
cols2 = st.lightColor(wls,flux=None,gamma=1,
                      irColor=[1,0,0,0.1], # you can specify what color you want for the IR
                      uvColor=[0.5,0,1,0.1]) # and UV


fig, axs = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)


for iwl in range(len(wls[:-1])):
    axs.fill_between([wls[iwl]*1e6,wls[iwl+1]*1e6], [f[iwl],f[iwl+1]],color=cols2[iwl],lw=0)
axs.set_xscale('log')
axs.set_yscale('log')


axs.set_xlim(wlim*1e6)
axs.set_ylim(np.min(f),np.max(f))

plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')

#%%%
fig, axs = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)

cmap=st.lightColorMap(uvColor=[0.5,0,1,1],irColor=[1,0,0,1],sfact=0.1,vfact=0.7)

axs.scatter(wls*1e6,f,c=wls,cmap=cmap,vmin=0.3e-6,vmax=0.8e-6)
axs.set_xscale('log')
axs.set_yscale('log')

axs.set_xlim(wlim*1e6)
axs.set_ylim(np.min(f),np.max(f))
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')

#%%