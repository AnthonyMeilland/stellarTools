# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 13:22:16 2020

@author: ame
"""


import stellarTools as st
import matplotlib.pyplot as plt

#Create a "typical" star with its spectral class
spClass="B3V"
star=st.typicalStar(spClass)

# Showing the parameters of the star
print(star)

# individual stellar parameters
Teff=star.Teff
Mstar=star.Mass
Rstar=star.Radius
Lstar=star.Lum
Vcrit=star.Vcrit

#Get and plot a kurucz model for such star at 100pc
dist = 100 #pc
kz=star.getKuruczModel(dist)

fig,ax = plt.subplots()
ax.loglog(kz.wl*1e6,kz.f)
ax.set_xlabel("$\\lambda$ ($\\mu$m)")
ax.set_ylabel("Flux (W/m$^3$)")
ax.set_title(f"Kurucz model for a {spClass} star at {dist}pc")
