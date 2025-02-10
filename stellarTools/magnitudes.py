# -*- coding: utf-8 -*-

import numpy as np
import astropy.units as u


def photometricFilter(band,typ="Johnson"):

    if typ=="Johnson":
        Bands=np.array(['U','B','V','R','I','J','H','K','L','M','N','Q'])
        wls=np.array([.36,.44,.55,.71,.97,1.25,1.6,2.22,3.54,4.8,10.6,21.])*u.micron
        F0=np.array([1823,4130,3781,2941,2635,1603,1075,667,288,170,36,9.4])*u.Jy
    elif typ=="2MASS":
        Bands=np.array(['J','H','Ks'])
        wls=np.array([1.235,1.662,2.159])*u.micron
        F0=np.array([1594,1024,666.7])*u.Jy
    elif typ== 'UKIRT':
        Bands=np.array(['V','I','J','H','K','L',"L'",'M','N','Q'])
        wls=np.array([0.5556,0.9,1.25,1.65,2.2,3.45,3.8,4.8,10.1,20])*u.micron
        F0=np.array([3540,2250,1600,1020,657,290,252,163,39.8,10.4])*u.Jy
    elif typ=='MIRLIN':
        Bands=np.array(['K','M','N0','N1','N2','N3','N4','N5','N','Qs','Q0','Q1','Q2','Q3','Q4','Q5'])
        wls=np.array([2.2,4.68,7.91,8.81,9.69,10.27,11.7,12.49,10.79,17.9,17.2,17.93,18.64,20.81,22.81,24.48])*u.micron
        F0=np.array([650,165,60.9,49.4,41.1,36.7,28.5,25.1,33.4,12.4,13.4,12.3,11.4,9.2,7.7,6.7])*u.Jy
    elif typ=='GAIA':
        Bands=np.array(['G'])
        wls=np.array([0.5857])*u.micron
        F0=np.array([2861])*u.Jy
        
    iBand=np.where(Bands==band)[0][0]
    return F0[iBand],wls[iBand]

#%%

class photUnit(u.Unit):
    def __init__(self,band,system):
        self.band=band
        self.F0, self.wl = photometricFilter(band,system)
        super.__init__(u.Jy)
        



def magPhot(band,typ="Johnson"):
    F0, wl = photometricFilter(band,typ)
    Flux=u.def_unit([f"Flux_{band}_{typ}"],F0 ,prefixes=False,doc="." )
    magF=u.MagUnit(Flux)
    magFSpecEquiv=u.equivalencies.spectral_density(wl)

    return magF,magFSpecEquiv,Fl



#%%
magV,spemagv=magPhot("V")


Fla=u.W/u.m**3
(0*magV).to(Fla,equivalencies=spemagv)

#%%

class photMag(object):
    def __init__(self,wlOrBand,F0=None,system=None,bandname=None):
        if isinstance(wlOrBand,str):
            band=wlOrBand
            wl=None
        else:
            wl=wlOrBand
            band=None
            
        if wl==None and  band==None:
            raise TypeError("Either wavelength (wl) or photometric band (band) should be specified")
        elif wl!=None and F0==None:
            raise TypeError("Zero-point flux (F0) shold be specified when using photMag with wavelength (wl)")
        elif band:
            if not(system):
                if band == "G":
                    system = "Gaia"
                elif band in "UBVRIJHKLMNQ":
                    system = "Johnson"
                else:
                    raise TypeError(f"Photometric system should be specified for filter {band}")
        
            self.F0, self.wl = photometricFilter(band,system)
            self.band = band
            
        else:
            self.F0 = F0
            self.wl = wl
            if not(bandname):
                self.band = wl.to_string().replace(" ","_")
            else:
                self.band = bandname
                
                
        if system == None:
            magname = f"Flux_{band}"
        else:
            magname = f"Flux_{band}_{system}"
        self.Flux=u.def_unit([magname],F0 ,prefixes=False,doc="." )
        self.mag=u.MagUnit(self.Flux)
        self.equivalency=u.equivalencies.spectral_density(wl)
    
    def to(self,unit, **kwarg):
        return self.mag.to(unit,equivalencies=self.equivalency)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        