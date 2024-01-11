# -*- coding: utf-8 -*-
"""
*******************************************************************************

Created on Mon Feb  1 10:39:11 2021

@author: Anthony Meilland

This module contains the sed class whic is a wrapping of the VO table from the 
Vizier SED web service. SEDs can be acquired from the web service, manipulated 
and saved to the VO format, load again later.

class sed:
    
"""

import requests as req
import numpy as np
import astropy.io.votable as vot
import os
import matplotlib.pyplot as plt
import astropy.units as u
#import stellarTools.typicalStar as typicalStar
from  astroquery.vizier import Vizier



fov0=5
filename_temp="temp.vot"


class sed:  
    
    def __init__(self,name=None,filename=None,fov=fov0):
       self.otherData=[]
       self.name=name
       self.excludedCatalogs=[]
       if name!=None:
           self.fromVizier(name,fov)
       if filename!=None:
           self.loadVOT(filename)
   
    def fromVizier(self,name,fov=fov0):
        resp = req.get(" https://vizier.u-strasbg.fr/viz-bin/sed?-c={0}&-c.rs={1:.2f} ".format(name,fov))
        txt=resp.text
        f=open(filename_temp,"w")
        f.write(txt)
        f.close()
        self.data=vot.parse(filename_temp).get_table_by_index(0).to_table()
        os.remove(filename_temp)
    
    def loadVOT(self,filename):
        self.data=vot.parse(filename).get_table_by_index(0).to_table()
  
    def saveVOT(self,filename):
        pass
             
    def flux(self,unit=u.Jy,dataOnly=False,filter=True):
        res=self.data["sed_flux"].to(unit,equivalencies=u.spectral_density(self.data["sed_freq"]))
        if filter==True:
            res=res[self._filtIdx()]
        if dataOnly==True:
            res=res.value
        return res
    
    def errflux(self,unit=u.Jy,dataOnly=False,filter=True):
        res=self.data["sed_eflux"].to(unit,equivalencies=u.spectral_density(self.data["sed_freq"]))
        if filter==True:
            res=res[self._filtIdx()]
        if dataOnly==True:
            res=res.value
        return res    
    
    def wl(self,unit=u.m,dataOnly=False,filter=True):
        res=self.data["sed_freq"].to(unit, equivalencies=u.spectral())

        if filter==True:
            res=res[self._filtIdx()]
        if dataOnly==True:
            res=res.value
        return res
    
    def excludeCatalogs(self,catnames):
        if type(catnames)==type(""):
            catnames=[catnames]
        self.excludedCatalogs.extend(catnames)
        
    def addCatalog(self,catname):
        if catname=="Jamar1976":
            self.otherData.append(_Jamar1976(self.name))
    
            
    def _filtIdx(self):
        catlist=self.data["_tabname"]
        if len(self.excludedCatalogs)==0:
            idx=np.arange(len(catlist))
        else:
            res=[]
            for excat in self.excludedCatalogs:
                resi=(catlist == excat)
                res.append(resi)
            res=np.sum(np.array(res),axis=0)
            idx=np.where(res==0)
        return idx
        
    def plot(self,filter=True,xunit=u.m,yunit=u.Jy,xscale="log",yscale="log",ax=None,errorbar=False,marker=".",ls="",**kwarg):
        if ax==None:
            fig,ax=plt.subplots()
        
        ax.plot(self.wl(xunit,dataOnly=True,filter=filter),
                self.flux(yunit,dataOnly=True,filter=filter),
                marker=marker,ls=ls,label="Vizier SED",**kwarg)
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)        
        

        for datai in self.otherData:
            try:
                ax.plot(datai.wl.to(xunit),datai.flux.to(yunit,equivalencies=u.spectral_density(datai.wl)),label=datai.catname)
            except:
                pass
            
        if xunit.physical_type=='length':
            valx="$\\lambda$"
        else:
            valx="$\\nu$"
                    
        
        if yunit.physical_type=='spectral flux density':
           
            valy="F$_\\nu$"
        else:
            valy="F$_\\lambda$"        
        
        ax.set_xlabel("{0} ({1})".format(valx,xunit.to_string("latex")))
        ax.set_ylabel("{0} ({1})".format(valy,yunit.to_string("latex")))
        
        
            
        
        return ax 
    
    

class _Jamar1976:
    def __init__(self,name):
        self.catname="Jamar (1976)"
        try:
            Viz=Vizier(columns=["**"])
            res=Viz.query_object(name,catalog="III/39A/catalog")
            
            cols=res[0].columns
            ncols=len(cols)
            isFlx=np.array([((cols[i].name[0]=="F") & (len(cols[i].name)==5))for i in range(ncols)])
            isE_Flx=np.array([((cols[i].name[0:3]=="e_F") & (len(cols[i].name)==7))for i in range(ncols)])
            
            self.wl=((np.array([cols[i].name[1:] for i in range(ncols) if isFlx[i]==True]).astype(float)*u.AA).to(u.m))[1:]
            self.flux=(np.array([res[0][cols[i].name].data.data[0] for i in range(ncols) if isFlx[i]==True]).astype(float)*1e-12*u.W/u.m**2/u.nm)[1:]
            self.flux=(self.flux.to(u.Jy,equivalencies=u.spectral_density(self.wl)))
            self.eflux=(np.array([res[0][cols[i].name].data.data[0] for i in range(ncols) if isE_Flx[i]==True]).astype(float)/100)[1:]
            self.eflux=self.eflux*self.flux
        except:
            print("No Jamar 1976 data on {0}".format(name))
        
class ines:
    def __init__(self,name=None,filename=None):
        if name!=None:
            self.getFromWeb(name)
        if filename!=None:
            self.loadFits(filename) 
        
    def getFromWeb(self,name):
        resp = req.get(" https:// ".format(name))
    
    
    def loadFits(self,filename):
        pass


def SEDsynth(wlin,fin,wlout):
    nwl=np.size(wlout)
    
    wlbin=[]
    fbin=[]
    fbinerr=[]
    for iwl in range(nwl):
        if iwl!=0:
            wlm=(wlout[iwl]+wlout[iwl-1])/2
        else:
            wlm=wlout[iwl]     
        if iwl!=nwl-1:
            wlp=(wlout[iwl]+wlout[iwl+1])/2
        else:
            wlp=wlout[iwl]
  
        idx=np.where((wlin > wlm) & (wlin<wlp) )[0]

        
        if len(idx)!=0:
            wlbin.append(wlout[iwl])
            fidx=np.take(fin,idx)
            fi=np.median(fidx)
            ferri=np.std(fidx)
            ferri=(np.max(fidx)-np.min(fidx))/2
            
            fbin.append(fi)
            fbinerr.append(ferri)
         
    wlbin=np.array(wlbin)
    fbin=np.array(fbin)        
    fbinerr=np.array(fbinerr)

    fout=10**np.interp(wlout,wlbin,np.log10(fbin))
    fouterr=10**np.interp(wlout,wlbin,np.log10(fbinerr))
    return wlout,fout,fouterr        
        
    