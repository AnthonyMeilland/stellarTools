# -*- coding: utf-8 -*-
"""
Created on Wed Nov 06 13:19:32 2013

@author: ame
"""

import stellarTools as st
import matplotlib.pyplot as plt

spClass=["B0V","B5V","A0V","A5V","F0V","F5V",
         "G0V","G5V","K0V","K5V","M0V","M5V"]


dist = 500 #pc

fig, ax = plt.subplots()

for spClassi in spClass:
    
    stari = st.typicalStar(spClassi)
    
    ki = stari.getKuruczModel(dist)
    
    
    ax.plot(ki.wl*1e6,ki.f,label=f"{spClassi} ({stari.Radius:.1f}R$_\\odot$" \
                                  f"- {stari.Teff:.0f}K)")

ax.set_title("Kurucz models for typical stars")
ax.set_xscale("log")
ax.set_ylim(1e-24,1e-7)
ax.set_yscale("log")
ax.set_xlim(0.08,100)
plt.legend(fontsize=8)
