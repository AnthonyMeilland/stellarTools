# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:33:29 2019

@author: ame
"""


import numpy as np

series_names=["Lyman","Balmer","Paschen","Brackett","Pfund","Humphreys","Hansen-Strong"]
series_shortname=["Ly","H","Pa","Br","Pf","Hu","Hs"]
series_letter=["\\alpha","\\beta","\\gamma","\\delta","\\epsilon"]


def getLine(n1,n2):
    Rh=1.09678e7
    if n1!=np.inf:
        lam=1./(Rh*(1./n2**2.-1./n1**2.))
    else:
        lam=n2**2./Rh
    return lam


def getLines(series,nlines,z=0):

    nseries=len(series)
    lines=[]
    for i in range(nseries):
        n2=series[i]
        if i<6:
            sname=series_shortname[n2-1]
        else:
            sname=n2
        for j in range(nlines):
            n1=n2+j+1
            lam=getLine(n1,n2)*(1.+z)
            if j<5:
                l=series_letter[j]
            else:
                l=n1#j+1


            name="{0}$_{{{1}}}$".format(sname,l)
            lines.append({'wl':lam,'name':name,'n1':n1,'n2':n2})
        lam=getLine(np.inf,n2)*(1.+z)
        name="{0}$_\infty$".format(sname)
        lines.append({'wl':lam,'name':name,'n1':np.inf,'n2':n2})

    return lines

